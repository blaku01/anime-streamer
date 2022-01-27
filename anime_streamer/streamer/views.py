from re import A
from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q, Count
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def anime_series(request):
    anime_series = AnimeSerie.objects.all()
    return render(request, 'home.html', {'anime_series': anime_series})


def anime_detail(request, title):
    anime = AnimeSerie.objects.get(title=title)
    genres = anime.anime_genre_tags.values_list('name', flat=True)
    simillar_anime = AnimeSerie.objects.filter(anime_genre_tags__in=genres).exclude(id=anime_series.id)

    return render(request, 'series_template.html', {'anime': anime, 'simillar_anime': simillar_anime})

def chapter_detail(request, title, chapter_number):
    anime = AnimeSerie.objects.filter(title=title)
    chapter = AnimeChapter.objects.filter(anime_serie=anime, chapter_number=chapter_number)

    return render(request, 'series_template', {'anime': anime, 'chapter' : chapter})

def video_detail(request, title, chapter_number, service):
    anime = AnimeSerie.objects.filter(title=title)
    chapter = AnimeChapter.objects.filter(anime_serie=anime, chapter_number=chapter_number)
    service = Video.objects.filter(anime_chapter=chapter, service=service)

    return render(request, 'series_template', {'anime': anime, 'chapter' : chapter })

def search_for_anime(request):
    search = request.GET.get('search', '')
    genres = request.GET.get('genres', '').split(sep=',')
    genres_exl = request.GET.get('genres_exl', 'a').split(sep=',')
    char_types = request.GET.get('char_types', '').split(sep=',')
    char_types_exl = request.GET.get('char_types_exl', 'a').split(sep=',')
    status = request.GET.get('status', '').split(sep=',')
    season = request.GET.get('season', '').split(sep=',')
    date_min = request.GET.get('date_min', '')
    date_max = request.GET.get('date_max', '')

    anime_series = AnimeSerie.objects \
    .filter(anime_genre_tags__name__in=genres).annotate(num_tags=Count('anime_genre_tags')).filter(num_tags__gte=len(genres)).distinct() \
    .exclude(anime_genre_tags__name__in=genres_exl).annotate(num_tags=Count('anime_genre_tags')).filter(num_tags__gte=len(genres_exl)).distinct() \
    .filter(character_type_tags__name__in=char_types).annotate(num_tags=Count('anime_genre_tags')).filter(num_tags__gte=len(char_types)).distinct() \
    .exclude(character_type_tags__name__in=char_types_exl).annotate(num_tags=Count('anime_genre_tags')).exclude(num_tags__gte=len(char_types_exl)).distinct() \


    return render(request, 'home.html', {'anime_series': anime_series})