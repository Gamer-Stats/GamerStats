from django.contrib import admin
from core.models import Wiki, WikiCategory, NewsCategory, ImageCollection, Topic


admin.site.register(Wiki)
admin.site.register(WikiCategory)
admin.site.register(NewsCategory)
admin.site.register(ImageCollection)
admin.site.register(Topic)
