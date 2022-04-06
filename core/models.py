from django.db import models


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

    class Meta:
        abstract = True


class Topic(BaseOptions):
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
