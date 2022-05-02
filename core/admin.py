from django.contrib import admin
from core.models import (
    JsonData,
    SEOImage,
    Subscribe,
    Wiki,
    WikiCategory,
    NewsCategory,
    ImageCollection,
    Topic,
    PcSpecs,
    SetupSettings,
    News,
)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]


@admin.register(ImageCollection)
class ImageCollectionAdmin(admin.ModelAdmin):
    search_fields = ("title", "image_type")
    list_filter = ["image_type"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    autocomplete_fields = ["avatar"]


@admin.register(PcSpecs)
class PcSpecsAdmin(admin.ModelAdmin):
    search_fields = ["title"]


@admin.register(JsonData)
class JsonDataAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_filter = ["data_type"]


@admin.register(WikiCategory)
class WikiCategoryAdmin(admin.ModelAdmin):
    search_fields = ["title"]


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    list_display = ("title", "avatar")
    search_fields = ["title"]
    list_filter = ["page_type"]
    autocomplete_fields = ("avatar", "info_box", "tags")


@admin.register(SetupSettings)
class SetupAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "meta_images", "game")
    list_filter = ["game"]
    autocomplete_fields = ("specs", "team", "related", "avatar")


admin.site.register(NewsCategory)
admin.site.register(SEOImage)
admin.site.register(Subscribe)
