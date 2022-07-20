from django import forms
from django.db import models
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail import blocks
from wagtail.admin.edit_handlers import ObjectList, TabbedInterface
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from wagtail.models import Orderable, Page
from wagtail.search import index

new_table_options = {
    'autoColumnSize': True,
    'mergeCells': True,
    'contextMenu': [
        'mergeCells',
        'row_above',
        'row_below',
        '---------',
        'col_left',
        'col_right',
        '---------',
        'remove_row',
        'remove_col',
        '---------',
        'undo',
        'redo',
        '---------',
        'copy',
        'cut'
        '---------',
        'alignment',
    ],
}


class ProfileIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro", classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        profilepages = self.get_children().live().order_by("live_revision")
        context["profilepages"] = profilepages
        return context


class Country(Page):
    iso = models.CharField(max_length=2)
    flag = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="flag_image",
        blank=True,
        null=True,
    )
    search_fields = Page.search_fields + [
        index.SearchField("title"),
    ]
    content_panels = Page.content_panels + [
        FieldPanel("iso"),
        FieldPanel("flag"),
    ]


class SettingsBlock(blocks.StructBlock):
    key_name = blocks.CharBlock(required=False)
    value_name = blocks.CharBlock(required=False)


class SettingsMain(Orderable):
    profile = ParentalKey(
        "ProfilePage",
        on_delete=models.SET_NULL,
        related_name="player_settings",
        null=True,
    )
    title = models.CharField(max_length=150, blank=True)
    profile_settings = StreamField(
        [
            (
                "section_settings",
                blocks.StructBlock(
                    [
                        ("sub_heading", blocks.CharBlock(required=False)),
                        ("section_details", blocks.ListBlock(SettingsBlock())),
                    ]
                ),
            )
        ],
        use_json_field=True,
        blank=True,
    )


class Specs(Orderable):
    PRODUCT_ITEMS = (
        ("CPU", "CPU"),
        ("GPU", "GPU"),
        ("RAM", "RAM"),
        ("SSD", "SSD"),
        ("CASE", "Case"),
        ("MB", "Motherboard"),
        ("PS", "Power Supply"),
        ("HDD", "Hard Drive"),
        ("KBD", "Keyboard"),
        ("MOU", "Mouse"),
        ("MON", "Monitor"),
        ("CAM", "Camera"),
        ("WEB", "WEBCAM"),
        ("SPE", "Speaker"),
        ("ARM", "ARM"),
        ("MIC", "Microphone"),
        ("MP", "Mousepad"),
        ("HS", "Headset"),
        ("CHAIR", "Chair"),
        ("LC", "Liquid Cooling"),
    )
    profile = ParentalKey(
        "ProfilePage", on_delete=models.SET_NULL, related_name="player_specs", null=True
    )
    product_type = models.CharField(max_length=150, blank=True, choices=PRODUCT_ITEMS)
    product_name = models.CharField(max_length=150, blank=True, null=True)
    product_image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="spec_image",
        blank=True,
        null=True,
    )
    amazon_url = models.URLField(blank=True, null=True)


class SocialMedia(Orderable):
    profile = ParentalKey(
        "ProfilePage",
        on_delete=models.SET_NULL,
        related_name="player_social",
        blank=True,
        null=True,
    )
    team = ParentalKey(
        "TeamPage",
        on_delete=models.SET_NULL,
        related_name="team_social",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=150, blank=True)
    icon = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="social_icon",
        blank=True,
        null=True,
    )
    url = models.URLField(blank=True, null=True)


class ProfilePage(Page):
    created_at = models.DateTimeField("Post date")
    updated_at = models.DateTimeField("Last updated", null=True)
    full_name = models.CharField(max_length=150, blank=True)
    native_name = models.CharField(max_length=150, blank=True)
    intro = RichTextField(null=True, blank=True)
    hometown = models.CharField(max_length=150, blank=True)
    birth_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    player_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="profile_country",
        blank=True,
        null=True,
    )
    avatar = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="profile_avatar",
        blank=True,
        null=True,
    )
    cover = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="profile_cover",
        blank=True,
        null=True,
    )

    player_rank = models.PositiveIntegerField(blank=True, null=True)
    text = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock(table_options=new_table_options)),
    ], use_json_field=True, null=True, blank=True)
    body = RichTextField(blank=True)
    earnings = models.PositiveIntegerField(blank=True, null=True)
    is_pro = models.BooleanField(default=False)
    player_role = models.CharField(max_length=150, blank=True, null=True)
    game = models.ForeignKey(
        "GamePage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="player_game",
    )
    team = models.ForeignKey(
        "TeamPage",
        on_delete=models.SET_NULL,
        related_name="player_team",
        blank=True,
        null=True,
    )

    related_profiles = ParentalManyToManyField('self', blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("created_at"),
        FieldPanel("updated_at"),
        FieldPanel("full_name"),
        FieldPanel("native_name"),
        FieldPanel("avatar"),
        FieldPanel("cover"),
        FieldPanel("hometown"),
        FieldPanel("player_rank"),
        FieldPanel("team"),
        FieldPanel("game"),
        FieldPanel("is_pro"),
        FieldPanel("player_role"),
        FieldPanel("birth_date"),
        FieldPanel("intro"),
        FieldPanel("start_date"),
        FieldPanel("end_date"),
        FieldPanel("player_country"),
        FieldPanel("earnings"),
        FieldPanel('text'),
        FieldPanel("body", classname="full"),
        InlinePanel("player_specs", label="Player Specs"),
        InlinePanel("player_settings", label="Player Settings"),
        InlinePanel("player_social", label="Player Social"),
    ]

    related_panel = [
        MultiFieldPanel(
            [
                FieldPanel('related_profiles', widget=forms.CheckboxSelectMultiple),
            ],
            heading="Related Profiles",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(content_panels, heading='Content'),
            ObjectList(related_panel, heading='Related Profiles'),
            ObjectList(Page.promote_panels, heading='SEO'),
            ObjectList(Page.settings_panels, heading='Settings'),
        ]
    )


class TeamPage(Page):
    created_at = models.DateTimeField("Post date", null=True, blank=True)
    updated_at = models.DateTimeField("Last updated", null=True, blank=True)
    abbr = models.CharField(max_length=50, blank=True)
    avatar = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="team_avatar",
        blank=True,
        null=True,
    )
    cover = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="team_cover",
        blank=True,
        null=True,
    )
    in_game_leader = models.ForeignKey(
        ProfilePage,
        on_delete=models.SET_NULL,
        related_name="team_leader",
        blank=True,
        null=True,
    )
    earnings = models.PositiveIntegerField(blank=True, null=True)
    team_info = StreamField(
        [
            (
                "section_settings",
                blocks.StructBlock(
                    [
                        ("key_name", blocks.CharBlock(required=False)),
                        ("key_value", blocks.CharBlock(required=False)),
                        ("key_url", blocks.CharBlock(required=False)),
                    ]
                ),
            )
        ],
        use_json_field=True,
        null=True,
        blank=True,
    )
    intro = RichTextField(blank=True, null=True)
    hometown = models.CharField(max_length=150, blank=True)
    text = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock(table_options=new_table_options)),
    ], use_json_field=True, null=True, blank=True)
    body = RichTextField(blank=True)
    team_country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        related_name="teamcountry",
        blank=True,
        null=True,
    )

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("created_at"),
        FieldPanel("updated_at"),
        FieldPanel("abbr"),
        FieldPanel("avatar"),
        FieldPanel("cover"),
        FieldPanel("in_game_leader"),
        FieldPanel("earnings"),
        FieldPanel("team_info"),
        FieldPanel("intro"),
        FieldPanel("hometown"),
        FieldPanel('text'),
        FieldPanel("body"),
        FieldPanel("team_country"),
        InlinePanel("team_social", label="Team Social"),
    ]


class GamePage(Page):
    created_at = models.DateTimeField("Post date", null=True)
    updated_at = models.DateTimeField("Last updated", null=True)
    full_name = models.CharField(max_length=100, blank=True)
    avatar = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="game_avatar",
        blank=True,
        null=True,
    )
    cover = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        related_name="game_cover",
        blank=True,
        null=True,
    )
    intro = RichTextField(blank=True, null=True)
    text = StreamField([
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('table', TableBlock(table_options=new_table_options)),
    ], use_json_field=True, null=True, blank=True)
    body = RichTextField(blank=True, null=True)

    search_fields = Page.search_fields + [
        index.SearchField("full_name"),
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("created_at"),
        FieldPanel("updated_at"),
        FieldPanel("full_name"),
        FieldPanel("avatar"),
        FieldPanel("cover"),
        FieldPanel("intro", classname="full"),
        FieldPanel('text'),
        FieldPanel("body", classname="full"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        teampages = self.get_children().live().order_by("last_published_at")
        players = ProfilePage.objects.filter(
            game=self.id
            ).live().order_by("player_rank")
        context["teampages"] = teampages
        context["players"] = players
        return context
