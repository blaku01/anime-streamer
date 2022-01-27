from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import apps
from . import views

app_name = apps.StreamerConfig.name
urlpatterns = [
    path("search/", views.search_for_anime, name="search-anime"),
    path("<str:title>/<int:chapter_number>/<str:service>/", views.video_detail, name = "watch-video"),
    path("<str:title>/<int:chapter_number>/", views.chapter_detail, name = "chapter-detail"),
    path("<str:title>/", views.anime_detail, name = "anime-detail"),
    path("", views.anime_series, name="anime-list")
]
