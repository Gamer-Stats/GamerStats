from django.db import models
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
        newpages = self.get_children().live().order_by("-last_published_at")
        context["newpages"] = newpages
        return context


class NewsCats(Page):
    intro = RichTextField(blank=True)
    bol = models.BooleanField(default=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
        FieldPanel('bol')
    ]

    def get_context(self, request):
        context = super().get_context(request)
        newpages = NewsPage.objects.live().order_by("-last_published_at").filter(
            category__slug=self.slug
            )
        context["newpages"] = newpages
        return context


class NewsPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    bol = models.BooleanField(default=False)
    category = models.ForeignKey(NewsCats, on_delete=models.SET_NULL, null=True, blank=True)
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
            FieldPanel('featured_image'),
            FieldPanel('intro'),
            FieldPanel('category'),
            FieldPanel('bol'),
        ], heading="Meta"),
        FieldPanel('body', classname="full"),
    ]
