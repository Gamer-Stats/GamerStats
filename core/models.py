from datetime import datetime

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.text import slugify
from jsoneditor.fields.django3_jsonfield import JSONField


def upload_dir(instance, filename):
    return "{0}/{1}/{2}/{3}".format(
        instance.get_image_type_display(),
        datetime.today().year,
        datetime.today().month,
        filename,
    ).lower()


class ImageCollection(models.Model):
    IMAGE_TYPES = (("N", "News"), ("S", "PcSpecs"), ("P", "Profile"), ("C", "Category"))
    title = models.CharField(max_length=70)
    image = models.ImageField(upload_to=upload_dir)
    image_type = models.CharField(max_length=1, choices=IMAGE_TYPES)
    caption = models.CharField(max_length=100, blank=True)
    alt = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return self.title + " > " + self.get_image_type_display()  # type: ignore


class SEOImage(models.Model):
    title = models.CharField(max_length=30)
    hd_image = models.ImageField(upload_to="hd/", blank=True)
    sd_image = models.ImageField(upload_to="sd/", blank=True)

    class Meta:
        verbose_name = "SEO Image"
        verbose_name_plural = "SEO Images"

    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=30)
    username = models.SlugField()
    bio = models.TextField()
    image = models.ImageField(upload_to="author/")
    twitter = models.URLField()
    linkedin = models.URLField()

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name


class JsonData(models.Model):
    DATA_TYPE = (("I", "Wiki Info"), ("S", "Player Settings"))
    title = models.CharField(max_length=25)
    data_type = models.CharField(max_length=1, choices=DATA_TYPE, default="S")
    data = JSONField(blank=True)

    class Meta:
        verbose_name = "JSON Data"
        verbose_name_plural = "JSON Data"

    def __str__(self):
        return self.title


class BaseOptions(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, blank=True)
    avatar = models.ForeignKey(
        ImageCollection,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True, null=True)
    index_page = models.BooleanField(default=True)
    publish = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BaseOptions, self).save(*args, **kwargs)


class Topic(BaseOptions):
    pass

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title


class WikiCategory(BaseOptions):
    CAT_LEVEL = (
        ("c", "Country"),
        ("t", "Teams"),
        ("p", "Players"),
    )
    cat_level = models.CharField(null=True, blank=True, choices=CAT_LEVEL, max_length=1)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="parent_cat",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Wiki Category"
        verbose_name_plural = "Wiki Categories"

    def __str__(self):
        return self.title


class Wiki(BaseOptions):
    full_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="For team and game, use small name like Na’Vi and CS:GO",
    )
    meta_images = models.ForeignKey(
        SEOImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seo_images_wiki",
    )
    info_box = models.ForeignKey(
        JsonData,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="wiki_info",
    )
    overview = RichTextUploadingField(blank=True)
    body = RichTextUploadingField(blank=True)
    history = RichTextUploadingField(blank=True)
    career = RichTextUploadingField(blank=True, null=True)
    team_history = RichTextUploadingField(blank=True, null=True)
    achievements = RichTextUploadingField(blank=True, null=True)
    controversies = RichTextUploadingField(blank=True, null=True)
    ref = RichTextField(blank=True)
    tags = models.ManyToManyField(WikiCategory, related_name="wiki_tags", blank=True)
    related = models.ManyToManyField("self", blank=True)
    page_type = models.ForeignKey(
        Topic, on_delete=models.PROTECT, related_name="wiki_topic"
    )
    writer = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="wiki_writer",
    )

    class Meta:
        verbose_name = "Wiki"
        verbose_name_plural = "Wikis"

    def __str__(self):
        return self.title + " > " + self.page_type.title  # type: ignore


class NewsCategory(BaseOptions):
    intro_body = models.ForeignKey(
        Wiki, on_delete=models.PROTECT, blank=True, null=True
    )

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"

    def __str__(self):
        return self.title


class News(BaseOptions):
    overview = RichTextField(blank=True)
    body = RichTextUploadingField(blank=True)
    ref = RichTextField(blank=True)
    tags = models.ManyToManyField(NewsCategory, related_name="news_tags", blank=True)
    writer = models.ForeignKey(
        Author,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="news_writer",
    )

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title


class PcSpecs(BaseOptions):
    SPECS_TYPE = (
        ("mon", "Monitor"),
        ("ms", "Mouse"),
        ("msp", "Mousepad"),
        ("key", "Keyboard"),
        ("hs", "Headset"),
        ("cpu", "CPU"),
        ("gpu", "GPU"),
        ("mb", "Motherboard"),
        ("ram", "RAM"),
        ("case", "Case/Tower"),
        ("hdd", "HDD"),
        ("ssd", "SSD"),
        ("ps", "Power Supply"),
        ("mic", "Microphone"),
        ("cam", "Camera"),
        ("wcam", "Webcam"),
        ("ch", "Chair"),
        ("lc", "Liquid Cooling"),
        ("fn", "Fans"),
        ("arm", "ARM"),
        ("sl", "Studio Light"),
        ("con", "Controller"),
        ("o", "Other"),
    )
    PC_SECTION = (
        ("O", "Others"),
        ("GG", "Gaming Gear"),
        ("GPS", "Gaming PC Setup"),
        ("SPS", "Streaming PC Setup"),
    )
    section = models.CharField(
        max_length=3,
        choices=PC_SECTION,
        default="O",
        help_text="""GG: Monitor, Mouse, Mousepad, Keyboard, Headset
        |===| GPS: CPU, GPU, MB, RAM, Case, HDD, SSD, PowerSupply, LCOOL, Fans
        |===| SPS: Second Mon, ARM, Mic, CAM, WebCam, Chair, Ctrl Panel, AMP,
        Studio Lit, Light Kit, USB""",
    )
    specs_type = models.CharField(max_length=10, choices=SPECS_TYPE, default="o")
    price = models.PositiveIntegerField(blank=True, null=True)
    amazon_url = models.URLField()
    reviews = RichTextField(blank=True)

    class Meta:
        verbose_name = "PC Specs"
        verbose_name_plural = "PC Specs"

    def __str__(self):
        return self.title


class SetupSettings(BaseOptions):
    is_pro = models.BooleanField(default=True)
    meta_images = models.ForeignKey(
        SEOImage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="seo_images_setup",
    )
    overview = RichTextField(blank=True)
    settings_body = RichTextField(blank=True)
    settings = models.ForeignKey(
        JsonData,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="player_settings",
    )
    setup_body = RichTextField(blank=True)
    specs = models.ManyToManyField(PcSpecs, related_name="person_specs", blank=True)
    ref = RichTextField(blank=True)
    team = models.ForeignKey(
        Wiki,
        on_delete=models.SET_NULL,
        related_name="related_team",
        null=True,
        blank=True,
    )
    game = models.ForeignKey(
        Wiki,
        on_delete=models.SET_NULL,
        related_name="related_game",
        null=True,
        blank=True,
    )
    related = models.ManyToManyField("self", blank=True)
    writer = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = "Setup and Settings"
        verbose_name_plural = "Setup and Settings"

    def __str__(self):
        return self.title


class Subscribe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()

    def __str__(self):
        return self.email
