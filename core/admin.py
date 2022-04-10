from django.contrib import admin
from core.models import (
    JsonData,
    SEOImage,
    Wiki,
    WikiCategory,
    NewsCategory,
    ImageCollection,
    Topic,
    PcSpecs,
    SetupSettings,
    News,
)


@admin.register(PcSpecs)
class PcSpecsAdmin(admin.ModelAdmin):
    search_fields = (
        "title",
        "type",
        "pk",
    )


@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
    search_fields = ["title"]


@admin.register(SetupSettings)
class SetupAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    autocomplete_fields = ("specs", "tags", "related")


admin.site.register(WikiCategory)
admin.site.register(NewsCategory)
admin.site.register(ImageCollection)
admin.site.register(Topic)
admin.site.register(News)
admin.site.register(SEOImage)
admin.site.register(JsonData)
