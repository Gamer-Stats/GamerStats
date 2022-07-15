from django.db import models
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.search import index


class NewsIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        context = super().get_context(request)
        newpages = self.get_children().live().order_by("last_published_at")
        context["newpages"] = newpages
        return context


class NewsPageTag(TaggedItemBase):
    content_object = ParentalKey('NewsPage',
                                 related_name='tagged_items',
                                 on_delete=models.CASCADE)


class NewsPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=NewsPageTag, blank=True)
    featured_image = models.ForeignKey(Image,
                                       on_delete=models.SET_NULL,
                                       related_name='news_image',
                                       blank=True,
                                       null=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('featured_image'),
            FieldPanel('intro'),
        ], heading="Meta"),
        FieldPanel('body', classname="full"),
    ]
