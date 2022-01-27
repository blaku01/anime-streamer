from django.contrib import admin

# Register your models here.

from .models import *


class AnimeSerieAdmin(admin.ModelAdmin):
    list_display = ('title', 'prequel', 'sequel')
    list_filter = ('character_type_tags', 'anime_genre_tags')
    search_fields = ('title', 'genres')
    ordering = ['title']


admin.site.register(AnimeSerie, AnimeSerieAdmin)


class AnimeChapterAdmin(admin.ModelAdmin):
    list_display = ('anime_serie', 'chapter_number', 'title', 'description', 'type', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('anime_serie', 'chapter_number')
    ordering = ['anime_serie']


admin.site.register(AnimeChapter, AnimeChapterAdmin)

admin.site.register(Video)

# TAGS
admin.site.register(AnimeGenreTag)
admin.site.register(ThemeTag)
