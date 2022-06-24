from itertools import chain

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.decorators.cache import cache_page

from core.models import (GameProfile, News, NewsCategory, SetupSettings,
                         TeamProfile, Wiki)


# Homepage
@cache_page(60 * 129600)
def index(request):
    players = SetupSettings.objects.filter(
        publish=True).values(
        "title",
        "slug",
        "image_url",
        "team_url",
        "team__slug",
        "game__slug",
        "game",
        "team__title",
        "team__meta_title").order_by("-updated_at").exclude(is_pro=False)
    cs_players = players.filter(game=1)[:10]
    valo_players = players.filter(game=2)[:10]
    teams = TeamProfile.objects.filter(publish=True).values(
        "title",
        "slug",
        "esports_game__title",
        "esports_game__slug",
        "image_url",
        "game_image_url"
    )[:10]

    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(publish=True)[:12]
    )

    template_name = "index.html"
    context = {"cs_players": cs_players, "teams": teams,
               "news": news, "valo_players": valo_players}

    return render(request, template_name, context)


# News Main
@cache_page(60 * 129600)
def news(request):
    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(publish=True)
    )
    news_cat = NewsCategory.objects.order_by(
        "-updated_at").only("title", "slug")
    news = list(chain(news))
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)

    template_name = "news.html"
    context = {"obj": obj, "news_cat": news_cat}
    return render(request, template_name, context)


# News Single
@cache_page(60 * 129600)
def news_single(request, slug):
    try:
        obj = (
            News.objects.select_related("writer", "avatar")
            .prefetch_related("tags")
            .get(slug=slug)
        )
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, template_name="404.html"))

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
@cache_page(60 * 129600)
def news_filter(request, slug):
    cats = get_object_or_404(NewsCategory, slug=slug)
    news = (
        News.objects.select_related("avatar", "writer")
        .order_by("-updated_at")
        .filter(Q(publish=True) & Q(tags=cats))
    )
    news_cat = NewsCategory.objects.order_by(
        "-updated_at").only("title", "slug")
    paginator = Paginator(news, 12)

    page_num = request.GET.get("page")
    obj = paginator.get_page(page_num)
    template_name = "news.html"
    context = {"news": news, "obj": obj, "cats": cats, "news_cat": news_cat}
    return render(request, template_name, context)


# Setup Main
@cache_page(60 * 129600)
def setup(request):
    setups = (
        SetupSettings.objects.select_related(
            "avatar", "game", "team", "writer")
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


# Setup Single
@cache_page(60 * 129600)
def setup_single(request, slug):
    try:
        obj = (
            SetupSettings.objects.select_related(
                "settings", "avatar", "meta_images", "game", "team", "writer"
            )
            .prefetch_related("specs", "specs__avatar")
            .get(slug=slug)
        )
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, template_name="404.html"))

    if obj.team:
        related = (
            SetupSettings.objects.select_related(
                "avatar", "game", "team", "writer"
            ).filter(Q(game=obj.game) & Q(team=obj.team))
            .exclude(title=obj.title)
            .select_related("avatar")
        )
        related_title = "Teammates"
        bread = "Pro Settings"
    else:
        related = (
            SetupSettings.objects.select_related(
                "avatar", "game", "team", "writer"
            ).filter(game=obj.game)
            .exclude(title=obj.title)
            .select_related("avatar")
        )[:8]
        related_title = "Related"
        bread = "Setup"

    template_name = "setup_single.html"
    context = {
        "obj": obj,
        "related": related,
        "related_title": related_title,
        "bread": bread,
    }
    return render(request, template_name, context)


# Wiki Main
@cache_page(60 * 129600)
def wiki(request):
    wikis = Wiki.objects.select_related(
        "portal", "country", "avatar", "page_type").filter(publish=True)

    wikis = Paginator(wikis, 20)

    page_num = request.GET.get("page")
    obj = wikis.get_page(page_num)

    template_name = "wiki.html"
    context = {"obj": obj}
    return render(request, template_name, context)


# Wiki Single
@cache_page(60 * 129600)
def wiki_single(request, slug):
    try:
        obj = Wiki.objects.select_related(
            "avatar", "page_type", "meta_images", "info_box", "writer"
        ).get(slug=slug, publish=True)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, template_name="404.html"))

    if obj.page_type.pk == 2 or obj.page_type.pk == 6:
        history_title = "Early Life"
        career_title = "Career"
        team_history_title = "Team History"
    elif obj.page_type.pk == 1:
        history_title = "Early Life"
        career_title = "Career"
        team_history_title = "Esports"
    elif obj.page_type.pk == 3:
        history_title = "History"
        career_title = "Organization"
        team_history_title = "Former Members"
    elif obj.page_type.pk == 4:
        history_title = "Gameplay"
        career_title = "Development"
        team_history_title = "Organization"

    cats = obj.tags.all()
    wikis = Wiki.objects.select_related(
        "avatar").filter(Q(tags=cats) & Q(publish=True))
    template_name = "wiki_single.html"
    context = {
        "obj": obj,
        "cats": cats,
        "wikis": wikis,
        "history_title": history_title,
        "career_title": career_title,
        "team_history_title": team_history_title,
    }
    return render(request, template_name, context)


# Game
@cache_page(60 * 129600)
def gameprofile(request, slug):
    try:
        obj = GameProfile.objects.get(slug=slug)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, template_name="404.html"))

    teams = (
        TeamProfile.objects.filter(esports_game=obj, publish=True)
        .select_related("avatar", "team_wiki")
        .order_by("-updated_at")
    )

    players = SetupSettings.objects.filter(
        publish=True, game=obj, is_pro=True).values(
        "title",
        "slug",
        "image_url",
        "team_url",
        "team__slug",
        "game__slug",
        "game",
        "team__title",
        "team__meta_title")[:20]

    template_name = "game.html"
    context = {"obj": obj, "teams": teams, "players": players}
    return render(request, template_name, context)

# Team Profile


@cache_page(60 * 129600)
def teamprofile(request, game_url, slug):
    try:
        obj = TeamProfile.objects.select_related(
            'avatar', 'team_wiki', 'esports_game'
        ).get(slug=slug, esports_game__slug=game_url)

        active_members = obj.active_members.filter(
            publish=True).order_by("-updated_at").select_related(
                'avatar', 'page_type')

        inactive_members = obj.inactive_members.filter(
            publish=True).order_by("-updated_at").select_related(
                'avatar', 'page_type')

        former_members = obj.former_members.filter(
            publish=True).order_by("-updated_at").select_related(
                'avatar', 'page_type')

        template_name = "team.html"
        context = {"obj": obj, "active_members": active_members,
                   "inactive_members": inactive_members,
                   "former_members": former_members}

        return render(request, template_name, context)

    except ObjectDoesNotExist:
        return HttpResponseNotFound(render(request, template_name="404.html"))


# Search
@cache_page(60 * 15)
def search(request):
    if request.method == "GET":
        query = request.GET.get("q")
        wiki = Wiki.objects.filter(
            Q(title__icontains=query) | Q(
                overview__icontains=query) & Q(publish=True)
        )
        players_cat = SetupSettings.objects.filter(
            Q(title__icontains=query) | Q(
                overview__icontains=query) & Q(publish=True)
        )
        count = len(wiki) + len(players_cat)

    template_name = "searched.html"
    context = {"players_cat": players_cat,
               "wiki": wiki, "query": query, "count": count}
    return render(request, template_name, context)


def customhandler404(request, exception, template_name='404.html'):
    response = render(request, template_name)
    response.status_code = 404
    return response
