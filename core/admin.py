from django.contrib import admin

from core.models import (
    Author,
    Game,
    ImageCollection,
    JsonData,
    News,
    NewsCategory,
    PcSpecs,
    SEOImage,
    SetupSettings,
    Stats,
    Subscribe,
    Topic,
    Wiki,
    WikiCategory,
)


@admin.action(description="Mark as published")
def make_published(modeladmin, request, queryset):
    queryset.update(publish=True)


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
    list_display = ["title", "publish"]
    list_filter = ["publish"]
    actions = [make_published]


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    list_display = ("title", "publish", "pk")
    search_fields = ["title"]
    list_filter = ["page_type", "publish"]
    autocomplete_fields = ("avatar", "info_box", "tags", "related")


@admin.register(SetupSettings)
class SetupAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "meta_images")
    list_filter = ["is_pro"]
    autocomplete_fields = ("specs", "avatar")


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "updated_at", "publish")
    list_filter = ["publish"]
    autocomplete_fields = ["game"]


@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "updated_at", "publish")
    list_filter = ["publish"]
    autocomplete_fields = ["name"]


admin.site.register(NewsCategory)
admin.site.register(SEOImage)
admin.site.register(Subscribe)
admin.site.register(Author)
