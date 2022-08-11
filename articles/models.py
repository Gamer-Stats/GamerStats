from django import forms
from django.db import models
from modelcluster.fields import ParentalManyToManyField
from wagtail import blocks
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Page
from wagtail.search import index


class ArticleIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro", classname="full")]

    def get_context(self, request):
        context = super().get_context(request)
        newpages = self.get_children().live().order_by("-last_published_at")
        context["newpages"] = newpages
        return context


class ArticlePage(Page):
    new_table_options = {
        "autoColumnSize": True,
        "mergeCells": True,
        "contextMenu": [
            "mergeCells",
            "row_above",
            "row_below",
            "---------",
            "col_left",
            "col_right",
            "---------",
            "remove_row",
            "remove_col",
            "---------",
            "undo",
            "redo",
            "---------",
            "copy",
            "cut" "---------",
            "alignment",
        ],
    }

    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    text = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("table", TableBlock(table_options=new_table_options)),
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )
    publication_date = models.DateField(
        "Publication date", auto_now_add=True, blank=True, null=True
    )
    keywords = ParentalManyToManyField(
        "wagtailcore.Page",
        blank=True,
        related_name="article_tags",
    )
    featured_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="article_image",
        blank=True,
        null=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("featured_image"),
                FieldPanel("intro"),
            ],
            heading="Meta",
        ),
        FieldPanel("text"),
        FieldPanel("body", classname="full"),
    ]

    tags_panel = [
        MultiFieldPanel(
            [
                FieldPanel("keywords", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Add Tags",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading="Content"),
            ObjectList(tags_panel, heading="Tags"),
            ObjectList(Page.promote_panels, heading="SEO"),
            ObjectList(Page.settings_panels, heading="Settings"),
        ]
    )

    def get_context(self, request):
        context = super().get_context(request)
        related_posts = (
            ArticlePage.objects.live()
            .exclude(id=self.id)
            .filter(keywords__in=self.keywords.all())
            .distinct()
        )
        context["related_posts"] = related_posts
        return context
