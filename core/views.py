from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Prefetch, Q, prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from core.forms import SubscribeForm
from core.models import News, NewsCategory, SetupSettings, Wiki, WikiCategory

# from django.views.decorators.cache import cache_page



# Homepage - half op
def index(request):
    settings = SetupSettings.objects.select_related("avatar", "game", "team").order_by("-updated_at").filter(publish=True)
    pro_settings = settings.filter(is_pro=True)[:8]
    
    wikis = Wiki.objects.select_related("avatar", "page_type").order_by("-updated_at").filter(publish=True)[:4]
    news = News.objects.select_related("avatar", "writer").order_by("-updated_at").filter(publish=True)[:5]

    template_name = "index.html"
    context = {"pro_settings": pro_settings, "wikis": wikis, "news": news}
    return render(request, template_name, context)


# News Main op
def news(request):
    news = News.objects.select_related("avatar", "writer").order_by("-updated_at").filter(publish=True)
    news_cat = NewsCategory.objects.order_by("-updated_at").only("title", "slug")
    news = list(chain(news))
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    template_name = "news.html"
    context = {"obj": obj, "news_cat": news_cat}
    return render(request, template_name, context)


# News Single op
def news_single(request, slug):
    obj = News.objects.select_related("writer", "avatar").prefetch_related("tags").get(slug=slug)
    news = News.objects.select_related("writer", "avatar").order_by("-updated_at").filter(publish=True).distinct()[:3]

    template_name = "news_single.html"
    context = {"obj": obj, "news": news}
    return render(request, template_name, context)


# News Tags/Category
def news_filter(request, slug):
    cats = get_object_or_404(NewsCategory, slug=slug)
    news = News.objects.filter(tags=cats).exclude(publish=False)
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    tags = paginator.get_page(page_num)
    template_name = "news_cat.html"
    context = {"news": news, "tags": tags, "cats": cats}
    return render(request, template_name, context)


# Setup Main - OP - PAGE DONE
# @cache_page(60 * 15)
def setup(request):
    setups = SetupSettings.objects.select_related("avatar", "game", "team").order_by("-updated_at").filter(publish=True)
    setups = list(chain(setups))
    cats = Wiki.objects.filter(Q(page_type=3) | Q(page_type=4)).select_related("page_type").only("title", "slug", "page_type")

    setups = Paginator(setups, 20)

    page_num = request.GET.get("page")
    obj = setups.get_page(page_num)

    template_name = "setup.html"
    context = {"obj": obj, "cats": cats}
    return render(request, template_name, context)


# Setup Tags/Category
def setup_filter(request, slug, url_type):
    obj = get_object_or_404(Wiki, Q(slug=slug) & (Q(page_type=3) | Q(page_type=4)))
    url_type = obj.page_type
    players = SetupSettings.objects.filter(Q(game=obj) | Q(team=obj)).distinct()
    paginator = Paginator(players, 20)

    page_num = request.GET.get("page")
    players_cat = paginator.get_page(page_num)
    template_name = "players_cat.html"
    context = {"players_cat": players_cat, "obj": obj, "url_type": url_type}
    return render(request, template_name, context)


# Setup Single - half op
def setup_single(request, slug):
    obj = SetupSettings.objects.select_related("settings", "avatar", "meta_images", "game", "team").prefetch_related("specs__avatar").get(slug=slug)
    teammates = SetupSettings.objects.filter(Q(game=obj.game) & Q(team=obj.team)).exclude(title=obj.title).select_related("avatar", "game")

    template_name = "player_setup.html"
    context = {"obj": obj, "teammates": teammates}
    return render(request, template_name, context)


# Wiki Main - OP - PAGE DONE
def wiki(request):
    wikis = Wiki.objects.select_related("avatar", "page_type").order_by("-updated_at").filter(publish=True)
    wiki_cat = WikiCategory.objects.order_by("-updated_at").only("title", "slug")[:30]
    wikis = list(chain(wikis))
    paginator = Paginator(wikis, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    template_name = "wiki.html"
    context = {"obj": obj, "wiki_cat": wiki_cat}
    return render(request, template_name, context)


# Wiki Category/Tag
def wiki_filter(request, slug):
    wiki_cat = get_object_or_404(WikiCategory, slug=slug, publish=True)
    wiki = Wiki.objects.filter(tags=wiki_cat).exclude(publish=False).distinct()
    paginator = Paginator(wiki, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    name = "wiki_cat"
    template_name = "wiki.html"
    context = {"obj": obj, "name": name, "wiki_cat": wiki_cat}
    return render(request, template_name, context)


# wiki single - h-op
def wiki_single(request, slug):
    obj = Wiki.objects.select_related("avatar", "page_type", "meta_images", "info_box", "writer").get(slug=slug, publish=True)
    cats = obj.tags.all()

    template_name = "wiki_single.html"
    context = {"obj": obj, "cats": cats}
    return render(request, template_name, context)


# Email Subscribe
def subscribe(request):
    if request.method == "POST":
        subs_form = SubscribeForm(request.POST)
        if subs_form.is_valid():
            return HttpResponse("You sucessfully joined the list!")
    else:
        subs_form = SubscribeForm()

    template_name = "base.html"
    context = {"subs_form": subs_form}
    return render(request, template_name, context)


# Search
def search(request):
    if request.method == "GET":
        query = request.GET.get("searched")
        wiki = Wiki.objects.filter(Q(title__icontains=query) | Q(overview__icontains=query)
                                   ).exclude(Q(page_type=3) | Q(page_type=4) | Q(publish=False))
        players_cat = SetupSettings.objects.filter(Q(title__icontains=query) | Q(overview__icontains=query) & Q(publish=True))
        count = len(wiki) + len(players_cat)

    template_name = "searched.html"
    context = {"players_cat": players_cat, "wiki": wiki, "query": query, "count": count}
    return render(request, template_name, context)
