from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify


class ImageCollection(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField()
    caption = models.CharField(max_length=50, blank=True)
    alt = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BaseOptions(models.Model):
    title = models.CharField(max_length=80)
    slug = models.SlugField(blank=True)
    avatar = models.ForeignKey(
        ImageCollection,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="%(app_label)s_%(class)s_related",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_title = models.CharField(max_length=70)
    meta_description = models.TextField(blank=True)
    canonical_url = models.URLField(blank=True, null=True)
    publish = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(BaseOptions, self).save(*args, **kwargs)


class Topic(BaseOptions):
    pass

    def __str__(self):
        return self.title


class WikiCategory(BaseOptions):
    pass

    def __str__(self):
        return self.title


class Wiki(BaseOptions):
    info_box = models.TextField(blank=True, help_text="will change")
    overview = models.TextField(blank=True)
    body = models.TextField(blank=True)
    ref = models.TextField(blank=True)
    tags = models.ManyToManyField(WikiCategory, related_name="wiki_tags")
    page_type = models.ForeignKey(Topic, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


class NewsCategory(BaseOptions):
    intro_body = models.ForeignKey(
        Wiki, on_delete=models.PROTECT, blank=True, null=True
    )

    def __str__(self):
        return self.title


class News(BaseOptions):
    overview = models.TextField(blank=True)
    body = models.TextField(blank=True)
    ref = models.TextField(blank=True)
    tags = models.ManyToManyField(NewsCategory, related_name="news_tags")

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
    specs_type = models.CharField(max_length=4, choices=SPECS_TYPE, default="o")
    amazon_url = models.URLField()
    reviews = models.TextField(blank=True)

    def __str__(self):
        return self.title


class SetupSettings(BaseOptions):
    overview = models.TextField(blank=True)
    settings_body = models.TextField(blank=True)
    settings = ArrayField(models.CharField(max_length=30, blank=True))
    setup_body = models.TextField(blank=True)
    specs = models.ManyToManyField(PcSpecs, related_name="person_specs")
    ref = models.TextField(blank=True)
    tags = models.ManyToManyField(Wiki, related_name="things_linked")

    def __str__(self):
        return self.title
