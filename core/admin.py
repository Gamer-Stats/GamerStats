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


admin.site.register(Wiki)
admin.site.register(WikiCategory)
admin.site.register(NewsCategory)
admin.site.register(ImageCollection)
admin.site.register(Topic)
admin.site.register(PcSpecs)
admin.site.register(SetupSettings)
admin.site.register(News)
admin.site.register(SEOImage)
admin.site.register(JsonData)
