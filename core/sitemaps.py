from django.contrib import sitemaps
from django.urls import reverse

from core.models import SetupSettings, News, Wiki


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 1.0
    changefreq = "weekly"
    protocol = "https"

    def items(self):
        return ["index", "news", "setup", "wiki"]

    def location(self, item):
        return reverse(item)


class SetupSettings_Sitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return SetupSettings.objects.filter(publish=True).order_by("-updated_at")

    def location(self, obj):
        return "/setup/" + obj.slug + "/"  # type: ignore

    def lastmod(self, obj):
        return obj.updated_at


class Wiki_Sitemap(sitemaps.Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Wiki.objects.filter(publish=True).order_by("-updated_at")

    def location(self, obj):
        return "/wiki/" + obj.slug + "/"  # type: ignore

    def lastmod(self, obj):
        return obj.updated_at


class News_Sitemap(sitemaps.Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"

    def items(self):
        return News.objects.filter(publish=True).order_by("-updated_at")

    def location(self, obj):
        return "/news/" + obj.slug + "/"  # type: ignore

    def lastmod(self, obj):
        return obj.updated_at
