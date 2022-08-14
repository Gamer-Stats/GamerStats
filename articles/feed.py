from django.contrib.syndication.views import Feed

from articles.models import ArticlePage


class RssLatestArticles(Feed):
    title = "Latest Gaming Guides"
    link = "/guides/"
    description = "Latest gaming guides, walkthrough, and more!"

    def items(self):
        return ArticlePage.objects.live().order_by("-first_published_at")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.intro

    def item_link(self, item):
        return item.url

    def item_pubdate(self, item):
        return item.first_published_at

    def item_updateddate(self, item):
        return item.last_published_at

    def item_guid(self, item):
        return "https://gamerstats.net{}".format(item.url)

    def item_author_name(self, item):
        return "Gamer Stats"
