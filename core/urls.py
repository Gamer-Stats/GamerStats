from django.urls import path
from core import views
from django.contrib.sitemaps.views import sitemap

from core.sitemaps import StaticViewSitemap, SetupSettings_Sitemap, Wiki_Sitemap, News_Sitemap

sitemaps = {
    "static": StaticViewSitemap,
    "setup_s": SetupSettings_Sitemap,
}

news_sitemaps = {
    "news_s": News_Sitemap,
}

wiki_sitemaps = {
    "wiki_s": Wiki_Sitemap,
}

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.search, name="search"),
    path("news/", views.news, name="news"),
    path("news/<slug:slug>/", views.news_single, name="news_single"),
    path("news/categories/<slug:slug>/", views.news_filter, name="news_filter"),
    path("setup/", views.setup, name="setup"),
    path("setup/<slug:slug>/", views.setup_single, name="setup_single"),
    path("setup/<url_type>/<slug:slug>/", views.setup_filter, name="setup_filter"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<slug:slug>/", views.wiki_single, name="wiki_single"),
    path("wiki/categories/<slug:slug>/", views.wiki_filter, name="wiki_filter"),
    # Sitemaps
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path("sitemap-news.xml", sitemap, {"sitemaps": news_sitemaps}, name="django.contrib.sitemaps.views.sitemap",),
    path("sitemap-wiki.xml", sitemap, {"sitemaps": wiki_sitemaps}, name="django.contrib.sitemaps.views.sitemap",)
]
