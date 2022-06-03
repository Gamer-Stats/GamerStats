from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from core.forms import SubscribeForm
from core.models import News, NewsCategory, SetupSettings, Wiki, WikiCategory

# from django.views.decorators.cache import cache_page


# Homepage - half op DONE
def index(request):
    settings = (
        SetupSettings.objects.select_related("avatar", "game", "team")
        .order_by("-updated_at")
        .filter(publish=True)
    )
    pro_settings = settings.filter(is_pro=True)[:12]

    wikis = (
        Wiki.objects.select_related("avatar", "page_type")
        .order_by("-updated_at")
        .filter(publish=True)[:4]
    )
    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(publish=True)[:5]
    )

    template_name = "index.html"
    context = {"pro_settings": pro_settings, "wikis": wikis, "news": news}
    return render(request, template_name, context)


# News Main op
def news(request):
    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(publish=True)
    )
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
    try:
        obj = (
            News.objects.select_related("writer", "avatar")
            .prefetch_related("tags")
            .get(slug=slug)
        )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)
    news = (
        News.objects.select_related("writer", "avatar")
        .order_by("-updated_at")
        .filter(publish=True)
        .distinct()[:3]
    )

    template_name = "news_single.html"
    context = {"obj": obj, "news": news}
    return render(request, template_name, context)


# News Tags/Category
def news_filter(request, slug):
    cats = get_object_or_404(NewsCategory, slug=slug)
    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(Q(publish=True) & Q(tags=cats))
    )
    news_cat = NewsCategory.objects.order_by("-updated_at").only("title", "slug")
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)
    template_name = "news.html"
    context = {"news": news, "obj": obj, "cats": cats, "news_cat": news_cat}
    return render(request, template_name, context)


# Setup Main - OP - PAGE DONE
# @cache_page(60 * 15)
def setup(request):
    setups = (
        SetupSettings.objects.select_related("avatar", "game", "team")
        .order_by("-updated_at")
        .filter(publish=True)
    )
    setups = list(chain(setups))

    setups = Paginator(setups, 32)

    page_num = request.GET.get("page")
    obj = setups.get_page(page_num)

    template_name = "setup.html"
    context = {"obj": obj}
    return render(request, template_name, context)


# Setup Single - half op DONE
def setup_single(request, slug):
    try:
        obj = (
            SetupSettings.objects.select_related(
                "settings", "avatar", "meta_images", "game", "team"
            )
            .prefetch_related("specs", "specs__avatar")
            .get(slug=slug)
        )
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    teammates = (
        SetupSettings.objects.filter(Q(game=obj.game) & Q(team=obj.team))
        .exclude(title=obj.title)
        .select_related("avatar")
    )

    template_name = "setup_single.html"
    context = {"obj": obj, "teammates": teammates}
    return render(request, template_name, context)


# Wiki Main - OP - PAGE DONE
def wiki(request):
    wikis = (
        Wiki.objects.select_related("avatar", "page_type")
        .order_by("-updated_at")
        .filter(publish=True)
    )
    cats = (
        WikiCategory.objects.filter(publish=True)
        .order_by("-updated_at")
        .select_related("parent")
    )
    wikis = list(chain(wikis))
    paginator = Paginator(wikis, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    template_name = "wiki.html"
    context = {"obj": obj, "cats": cats}
    return render(request, template_name, context)


# Wiki Category/Tag
def wiki_filter(request, slug):
    cats_page = get_object_or_404(WikiCategory, slug=slug, publish=True)
    wiki = Wiki.objects.filter(Q(publish=True) & Q(tags=cats_page))

    cats = (
        WikiCategory.objects.filter(publish=True)
        .order_by("-updated_at")
        .select_related("parent")
    )

    paginator = Paginator(wiki, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    name = "cats"
    template_name = "wiki.html"
    context = {"obj": obj, "name": name, "cats_page": cats_page, "cats": cats}
    return render(request, template_name, context)


# wiki single - h-op
def wiki_single(request, slug):
    try:
        obj = Wiki.objects.select_related(
            "avatar", "page_type", "meta_images", "info_box", "writer"
        ).get(slug=slug, publish=True)
    except ObjectDoesNotExist:
        return HttpResponse(status=404)

    cats = obj.tags.all()
    wikis = Wiki.objects.select_related("avatar").filter(Q(tags=cats) & Q(publish=True))
    template_name = "wiki_single.html"
    context = {"obj": obj, "cats": cats, "wikis": wikis}
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
        wiki = Wiki.objects.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        ).exclude(Q(page_type=3) | Q(page_type=4) | Q(publish=False))
        players_cat = SetupSettings.objects.filter(
            Q(title__icontains=query) | Q(overview__icontains=query) & Q(publish=True)
        )
        count = len(wiki) + len(players_cat)

    template_name = "searched.html"
    context = {"players_cat": players_cat, "wiki": wiki, "query": query, "count": count}
    return render(request, template_name, context)
