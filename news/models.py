from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
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


class NewsPage(Page):
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ParentalManyToManyField(
        'wagtailcore.Page',
        blank=True,
        related_name='+',
    )
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
        ], heading="Meta"),
        FieldPanel('body', classname="full"),
    ]

    tags_panel = [
        MultiFieldPanel(
            [
                FieldPanel('tags', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Add Tags",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(tags_panel, heading='Tags'),
            ObjectList(Page.promote_panels, heading='SEO'),
            ObjectList(Page.settings_panels, heading='Settings'),
        ]
    )
