from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Count

# Create your views here.

def anime_serie_view(request, title):
    anime_series = get_object_or_404(AnimeSerie, title=title)
    anime_chapters = anime_series.animechapter_set.all()

    anime_series_genres_ids = anime_series.genres.values_list('id', flat=True)
    simillar_anime_series = AnimeSerie.objects.filter(genres__in=anime_series_genres_ids).exclude(id=anime_series.id)
    print(Count('genres'))
    simillar_anime_series = simillar_anime_series.annotate(same_genres=Count('genres')).order_by()
    return render(request, 'series_template.html',
                  {'series': anime_series, 'chapters': anime_chapters, 'simillar_anime_series': simillar_anime_series})
def anime_chapter_view():
    return

def anime_video_view():
    return