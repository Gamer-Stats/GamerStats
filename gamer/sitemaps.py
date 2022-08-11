from articles.models import ArticlePage
from django.contrib.sitemaps import Sitemap
from home.models import HomePage
from news.models import NewsPage
from profiles.models import GamePage, ProfileIndexPage, ProfilePage, TeamPage


class NewsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.7
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = NewsPage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = ArticlePage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class ProfileSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = ProfilePage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class TeamSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = TeamPage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class GameSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = GamePage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class HomeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = HomePage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at


class ProfileIndexSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = ProfileIndexPage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at
