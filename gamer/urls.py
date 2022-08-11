from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.decorators.cache import cache_page
from search import views as search_views
from wagtail import urls as wagtail_urls
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls

from gamer.sitemaps import (
    ArticleSitemap,
    GameSitemap,
    HomeSitemap,
    NewsSitemap,
    ProfileIndexSitemap,
    ProfileSitemap,
    TeamSitemap,
)

article_sitemaps = {
    "articlesitemap": ArticleSitemap,
}

news_sitemaps = {
    "newssitemap": NewsSitemap,
}

players_sitemaps = {
    "playerssitemap": ProfileSitemap,
}

teams_sitemaps = {
    "teamssitemap": TeamSitemap,
}

games_sitemaps = {
    "gamessitemap": GameSitemap,
}

page_sitemaps = {
    "static": HomeSitemap,
}

profile_index_sitemaps = {
    "profile_index": ProfileIndexSitemap,
}

urlpatterns = [
    path(
        "sitemap-articles.xml",
        sitemap,
        {"sitemaps": article_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-setup.xml",
        sitemap,
        {"sitemaps": profile_index_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-pages.xml",
        sitemap,
        {"sitemaps": page_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-news.xml",
        sitemap,
        {"sitemaps": news_sitemaps, "template_name": "news_sitemap.xml"},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-players.xml",
        sitemap,
        {"sitemaps": players_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-teams.xml",
        sitemap,
        {"sitemaps": teams_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "sitemap-games.xml",
        sitemap,
        {"sitemaps": games_sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # Add debug toolbar
    urlpatterns = urlpatterns + [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
