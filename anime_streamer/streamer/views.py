from re import A
from django.shortcuts import render, get_object_or_404
from .models import *
from django.db.models import Q, Count
from django.contrib.contenttypes.models import ContentType
import datetime
# Create your views here.

def anime_series(request):
    anime_series = AnimeSerie.objects.all()
    every_genre = AnimeGenreTag.objects.all()
    every_char_type = ThemeTag.objects.all()
    every_status = [x[1] for x in AnimeSerie.STATUSES]
    every_season = [x[1] for x in AnimeSerie.SEASONS]
    return render(request, 'home.html', {'anime_series': anime_series, 'every_genre': every_genre, 'every_char_type':every_char_type, 'every_status':every_status, 'every_season':every_season})

def anime_detail(request, title):
    anime = get_object_or_404(AnimeSerie, title=title)
    genres = anime.anime_genre_tags.values_list('name', flat=True)
    simillar_anime = AnimeSerie.objects.filter(anime_genre_tags__in=genres).exclude(id=anime.id)
    chapters = AnimeChapter.objects.filter(anime_serie=anime)

    return render(request, 'anime_detail.html', {'anime': anime, 'simillar_anime': simillar_anime,'chapters': chapters})

def chapter_detail(request, title, chapter_number):
    anime = get_object_or_404(AnimeSerie, title=title)
    chapter = get_object_or_404(AnimeChapter, anime_serie=anime, chapter_number=chapter_number)
    videos = Video.objects.filter(anime_chapter=chapter)
    return render(request, 'chapter_detail.html', {'anime': anime, 'anime_chapter' : chapter, 'videos':videos})

def video_detail(request, title, chapter_number, service):
    anime = get_object_or_404(AnimeSerie, title=title)
    chapter = get_object_or_404(AnimeChapter, anime_serie=anime, chapter_number=chapter_number)
    video = get_object_or_404(Video, anime_chapter=chapter, service=service)
    return render(request, 'videos_template.html', {'anime': anime, 'anime_chapter' : chapter, 'video':video})

def search_for_anime(request):
    every_genre = AnimeGenreTag.objects.all()
    every_char_type = ThemeTag.objects.all()
    every_status = [x[1] for x in AnimeSerie.STATUSES]
    every_season = [x[1] for x in AnimeSerie.SEASONS]
    search = request.GET.get('search', '')
    genres = request.GET.get('genres', '').split(sep=',')
    genres_exl = request.GET.get('genres_exl', '').split(sep=',')
    char_types = request.GET.get('char_types', '').split(sep=',')
    char_types_exl = request.GET.get('char_types_exl', '').split(sep=',')
    status = request.GET.get('status', '').split(sep=',')
    season = request.GET.get('season', '').split(sep=',')
    year_min, month_min, day_min = request.GET.get('date_min', '1000-01-01').split(sep='-')
    year_max, month_max, day_max = request.GET.get('date_max', '9999-12-30').split(sep='-')
    year_min, month_min, day_min, year_max, month_max, day_max = [int(x) for x in [year_min, month_min, day_min, year_max, month_max, day_max]]
    anime_series = AnimeSerie.objects.all()
    if search:
        anime_series = anime_series.filter(title__trigram_similar=search)
    if genres != ['']:
        anime_series = anime_series.filter(anime_genre_tags__name__in=genres).annotate(num_tags=Count('anime_genre_tags')).filter(num_tags__gte=len(genres))
    if char_types != ['']:
        anime_series = AnimeSerie.objects.filter(character_type_tags__name__in=char_types).annotate(num_tags=Count('character_type_tags')).filter(num_tags__gte=len(char_types))

    anime_series = anime_series.exclude(anime_genre_tags__name__in=genres_exl).annotate(num_tags=Count('anime_genre_tags')).filter(num_tags__gte=len(genres_exl)) \
    .exclude(character_type_tags__name__in=char_types_exl).annotate(num_tags=Count('character_type_tags')).filter(num_tags__gte=len(char_types_exl))

    if status != [''] :
        anime_series = anime_series.filter(status__in=status)
    if season != ['']:
        anime_series = anime_series.filter(season__in=season)
    
    if year_min:
        anime_series = anime_series.filter(released_at__gte=datetime.date(year_min, month_min, day_min))
    if year_max:
        anime_series = anime_series.filter(released_at__lte=datetime.date(year_max, month_max, day_max))

    anime_series = anime_series.distinct()

    return render(request, 'home.html', {'anime_series': anime_series, 'every_genre': every_genre, 'every_char_type':every_char_type, 'every_status':every_status, 'every_season':every_season})
