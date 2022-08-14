from django.db import models


class BaseModel(models.Model):
    """
    BaseModel class that provides created_at and updated_at fields
    """

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    intro = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="images/", blank=True, default="images/default.jpg"
    )
    seo_title = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    table = models.JSONField(blank=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    class Meta:
        abstract = True


class Game(BaseModel):
    """
    Game model
    """

    class Meta:
        verbose_name = "Game"
        verbose_name_plural = "Games"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.slug}/"


class PageCategory(models.Model):
    """
    PageCategory class that provides fields for game categories
    """
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, related_name="categories")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Game Category"
        verbose_name_plural = "Game Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.game.slug}/{self.slug}/"


class Page(BaseModel):
    """
    Page class for all types of game pages
    """
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, blank=True, related_name="pages")
    category = models.ForeignKey(PageCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="posts")
    is_pro = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f"/{self.game.slug}/{self.category.slug}/{self.slug}/"


class PageHelper(models.Model):
    """
    PageHelper class for Page in specical pages
    """
    description = models.TextField(blank=True)
    key = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, related_name="page_key")
    value = models.ManyToManyField(Page, null=True, blank=True, related_name="page_value")

    class Meta:
        verbose_name = "Event TG"
        verbose_name_plural = "Event TG"

    def __str__(self):
        return self.description
