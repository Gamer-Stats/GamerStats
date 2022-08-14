from django.urls import path

from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:game__slug>/<str:category__slug>/<str:slug>/", views.page, name="page"),
    path("<str:game__slug>/<str:slug>/", views.page_category, name="page_category"),
]
