from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist

from core.models import News, NewsCategory, SetupSettings, Wiki, WikiCategory

from core.forms import SubscribeForm


# Homepage
def index(request):
    ss = SetupSettings.objects.all()[:9]
    wikis = Wiki.objects.all().exclude(Q(page_type=3) | Q(page_type=4))[:3]
    news = News.objects.all()[:7]

    template_name = "index.html"
    context = {"ss": ss, "wikis": wikis, "news": news}
    return render(request, template_name, context)


# News Main
def news(request):
    news = News.objects.all()
    template_name = "news_cat.html"
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    tags = paginator.get_page(page_num)
    context = {"news": news, "tags": tags}
    return render(request, template_name, context)


# News Single
def news_single(request, slug):
    obj = get_object_or_404(News, slug=slug, publish=True)
    news = News.objects.all().exclude(title=obj)[:3]

    template_name = "news_single.html"
    context = {"obj": obj, "news": news}
    return render(request, template_name, context)


# News Tags/Category
def news_filter(request, slug):
    cats = get_object_or_404(NewsCategory, slug=slug)
    news = News.objects.filter(tags=cats)
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    tags = paginator.get_page(page_num)
    template_name = "news_cat.html"
    context = {"news": news, "tags": tags, "cats": cats}
    return render(request, template_name, context)


# Setup Main
def setup(request):
    setups = SetupSettings.objects.all()
    paginator = Paginator(setups, 20)

    page_num = request.GET.get("page")
    players_cat = paginator.get_page(page_num)

    obj = "Streamers and Esports"
    template_name = "players_cat.html"
    context = {"players_cat": players_cat, "obj": obj}
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


# Setup Single
def setup_single(request, slug):
    obj = get_object_or_404(SetupSettings, slug=slug)

    if obj.is_pro:
        teammates = SetupSettings.objects.filter(
            Q(team=obj.team) & Q(game=obj.game)
        ).exclude(title=obj.title)
    else:
        teammates = obj.related.all()  # type: ignore

    try:
        wiki = Wiki.objects.get(title=obj.title)
    except ObjectDoesNotExist:
        wiki = None

    template_name = "player_setup.html"
    context = {"obj": obj, "teammates": teammates, "wiki": wiki}
    return render(request, template_name, context)


# Wiki Main
def wiki(request):
    wikis = Wiki.objects.all().exclude(Q(page_type=3) | Q(page_type=4))
    paginator = Paginator(wikis, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    name = "wiki_main"
    template_name = "wiki.html"
    context = {"obj": obj, "name": name}
    return render(request, template_name, context)


# Wiki Category/Tag
def wiki_filter(request, slug):
    wiki_cat = get_object_or_404(WikiCategory, slug=slug)
    wiki = Wiki.objects.filter(tags=wiki_cat).distinct()
    paginator = Paginator(wiki, 20)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    name = "wiki_cat"
    template_name = "wiki.html"
    context = {"obj": obj, "name": name, "wiki_cat": wiki_cat}
    return render(request, template_name, context)


# Wiki Single
def wiki_single(request, slug):
    obj = get_object_or_404(Wiki, slug=slug, publish=True)

    template_name = "wiki_single.html"
    context = {"obj": obj}
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
                                   ).exclude(Q(page_type=3) | Q(page_type=4))
        players_cat = SetupSettings.objects.filter(Q(title__icontains=query) | Q(overview__icontains=query))
        count = len(wiki) + len(players_cat)

    template_name = "searched.html"
    context = {"players_cat": players_cat, "wiki": wiki, "query": query, "count": count}
    return render(request, template_name, context)
