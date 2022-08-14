from django.shortcuts import get_object_or_404, render

from core.models import Game, Page, PageCategory


def index(request):
    return render(request, "core/index.html")

def page(request, game__slug, category__slug, slug):
    page = Page.objects.get(game__slug=game__slug, category__slug=category__slug, slug=slug)
    return render(request, "core/page.html", {"page": page})


def page_category(request, game__slug, slug):
    game = get_object_or_404(Game, slug=game__slug)
    category = get_object_or_404(PageCategory, slug=slug)
    pages = Page.objects.filter(category=category)
    return render(request, "core/page_category.html", {"game": game, "category": category, "pages": pages})
