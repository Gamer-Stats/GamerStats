from django.contrib.sitemaps import Sitemap
from news.models import NewsPage


class NewsSitemap(Sitemap):
    changefreq = "never"
    priority = 0.8
    protocol = "https"

    def location(self, obj):
        return obj.url

    def items(self):
        obj = NewsPage.objects.filter(live=True)
        return obj

    def lastmod(self, obj):
        return obj.last_published_at
