from django.contrib import admin

from core.models import (Author, GameProfile, ImageCollection, JsonData, News,
                         NewsCategory, PcSpecs, SEOImage, SetupSettings,
                         TeamProfile, Topic, Wiki, WikiCategory)


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
    list_display = ("title", "avatar", "publish", "pk")
    search_fields = ["title"]
    list_filter = ["page_type", "publish"]
    autocomplete_fields = ("avatar", "info_box", "tags", "related")


@admin.register(SetupSettings)
class SetupAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "team", "game", "publish", "is_pro")
    list_filter = ["is_pro"]
    autocomplete_fields = ("specs", "avatar")
    readonly_fields = ["image_url"]


@admin.register(GameProfile)
class GameProfileAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "updated_at", "publish")
    list_filter = ["publish"]
    autocomplete_fields = ["game_wiki"]


@admin.register(TeamProfile)
class TeamProfileAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = ("title", "esports_game", "updated_at", "publish")
    list_filter = ["publish", "esports_game"]
    autocomplete_fields = ["team_wiki", "esports_game",
                           "active_members", "inactive_members", "former_members"]


admin.site.register(NewsCategory)
admin.site.register(SEOImage)
admin.site.register(Author)
