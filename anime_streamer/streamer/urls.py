from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import apps
from . import views

app_name = apps.StreamerConfig.name
urlpatterns = [
    path("<str:title>/<int:chapter_number>/<str:service>/", views.anime_video_view, name = "ViewVideo"),
    path("<str:title>/<int:chapter_number>/", views.anime_chapter_view, name = "ViewChapter"),
    path("<str:title>/", views.anime_serie_view, name = "ViewSerie"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
