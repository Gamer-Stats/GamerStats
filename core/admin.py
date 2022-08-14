from django.contrib import admin

from core.models import Game, Page, PageCategory


class GameAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "updated_at"]
    list_filter = ["updated_at"]
    search_fields = ["title", "slug"]
    ordering = ["-updated_at"]
    prepopulated_fields = {"slug": ("title",)}


class PageCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "updated_at"]
    list_filter = ["updated_at"]
    search_fields = ["title", "slug"]
    ordering = ["-updated_at"]
    prepopulated_fields = {"slug": ("name",)}


class PageAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "updated_at", "is_published"]
    list_filter = ["updated_at"]
    search_fields = ["title", "slug"]
    ordering = ["-updated_at"]
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Game, GameAdmin)
admin.site.register(PageCategory, PageCategoryAdmin)
admin.site.register(Page, PageAdmin)
