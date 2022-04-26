from django.urls import path
from core import views

urlpatterns = [
    path("", views.index, name="index"),
    path("news/", views.news, name="news"),
    path("news/<slug:slug>/", views.news_single, name="news_single"),
    path("news/single/<slug:slug>/", views.news_filter, name="news_filter"),
    path("setup/", views.setup, name="setup"),
    path("setup/<slug:slug>/", views.setup_single, name="setup_single"),
    path("setup/<url_type>/<slug:slug>/", views.setup_filter, name="setup_filter"),
    path("wiki/", views.wiki, name="wiki"),
    path("wiki/<slug:slug>/", views.wiki_single, name="wiki_single")
]
