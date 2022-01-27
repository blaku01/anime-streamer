from random import choices
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone, dateformat
from django.urls import reverse

from taggit.managers import TaggableManager
from taggit.models import TagBase, GenericTaggedItemBase
from gdstorage.storage import GoogleDriveStorage

from .managers import NoFillerManager

gd_storage = GoogleDriveStorage()

class AnimeGenreTag(TagBase):

    class Meta:
        verbose_name = _("AnimeGenreTag")
        verbose_name_plural = _("AnimeGenreTags")


class ThemeTag(TagBase):

    class Meta:
        verbose_name = _("ThemeTag")
        verbose_name_plural = _("ThemeTags")


class TaggedAnimeGenre(GenericTaggedItemBase):
    tag = models.ForeignKey(
        AnimeGenreTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )

class TaggedCharacterType(GenericTaggedItemBase):
    tag = models.ForeignKey(
        ThemeTag,
        on_delete=models.CASCADE,
        related_name="%(app_label)s_%(class)s_items",
    )



class AnimeSerie(models.Model):
    STATUSES = [
        ('Airing', 'Airing'),
        ('Finished', 'Finished'),
        ('Upcomming', 'Upcomming'),
        ('No-Upcomming', 'No-Upcomming'),
    ]

    TYPES = [
        ('Movie', 'Movie'),
        ('Serial', 'Serial'),
        ('ONA', 'ONA'),
        ('OVA', 'OVA'),
    ]

    SEASONS = [
        ('Fall', 'Fall'),
        ('Spring', 'Spring'),
        ('Summer', 'Summer'),
        ('Winter', 'Winter'),
    ]



    title = models.CharField(max_length=255, unique=True)
    prequel = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_prequel")
    sequel = models.ForeignKey('self', blank=True,null=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_sequel")
    status = models.CharField(max_length=31, null=True, choices=STATUSES)
    type = models.CharField(max_length=31, null=True, choices=TYPES)

    released_at = models.DateField(_("Date"), default=dateformat.format(timezone.now(), 'Y-m-d'))
    season = models.CharField(max_length=31, blank=True, null=True, choices=SEASONS)
    created_at=models.DateTimeField(blank=True, null=True, auto_now_add=True)

    anime_genre_tags = TaggableManager(through=TaggedAnimeGenre)
    character_type_tags = TaggableManager(through=TaggedCharacterType)
    thumbnail_image = models.ImageField(upload_to="anime_thumbnails/", storage=gd_storage, blank=True, null=True)

    objects = models.Manager()

    class Meta:
        ordering = ['title', '-released_at']

    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse("streamer:anime-detail", kwargs={"title": self.title})


class AnimeChapter(models.Model):
    TYPES = [
        ('Filler', 'Filler'),
        ('Manga', 'Based on manga'),
        ('Light Novel', 'Based on Light Novel')
    ]
    SUB = [
        (True, 'Subbed'),
        (False, 'Dubbed'),
    ]

    chapter_number = models.IntegerField(null=True)
    previous_chapter = models.ForeignKey('self', blank=True,null=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_previous_chapter")
    next_chapter = models.ForeignKey('self', blank=True,null=True, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_next_chapter")
    title = models.CharField(max_length=255)
    description = models.TextField( blank=True, null=True, default="currently n/a")
    anime_serie = models.ForeignKey(AnimeSerie, null=True, on_delete=models.CASCADE)
    type = models.CharField(max_length=31, null=True, choices=TYPES)

    created_at=models.DateTimeField(blank=True, null=True, auto_now_add=True)
    
    objects = models.Manager()
    no_filler = NoFillerManager()

    subbed = models.BooleanField(choices=SUB, blank=False)

    class Meta:
        ordering = ['anime_serie', 'chapter_number']

    def __str__(self):
        return str(self.anime_serie) + " " + str(self.chapter_number) + " " + str(self.title)

    def get_absolute_url(self):
        return reverse("streamer:chapter-detail", kwargs={"title": self.anime_serie.title, "chapter_number": self.chapter_number})

    
class Video(models.Model):
    QUALITY = [
        ('240p', '240p'),
        ('360p', '360p'),
        ('480p', '480p'),
        ('720p', '720p'),
        ('1080p', '1080p'),
        ('4K', '4K'),
    ]
    LANGUAGES = (
        ("pl", "Polish"),
        ("en", "English"),
        ("ja", "Japanese"),
        ("zh", "Chinese"),
        ("de", "German"),
    )

    service = models.CharField(max_length=255)
    quality = models.CharField(max_length=31, null=True, choices=QUALITY)
    voice_lang = models.CharField(max_length=31, null=True, choices=LANGUAGES)
    sub_lang = models.CharField(max_length=31, null=True, choices=LANGUAGES)
    created_at=models.DateTimeField( blank=True, null=True, auto_now_add=True)
    video_link = models.URLField(max_length=255)
    anime_chapter = models.ForeignKey(AnimeChapter, null=True, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        return str(self.anime_chapter) + " " + str(self.service)

    class Meta:
        ordering = ['created_at']
    
    def get_absolute_url(self):
        return reverse("streamer:watch-video", kwargs={"title":self.anime_chapter.anime_serie.title, "chapter_number": self.anime_chapter.chapter_number, "service": self.service})