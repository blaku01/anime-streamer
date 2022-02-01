from django.test import TestCase, Client
from ..models import AnimeSerie, AnimeChapter, TaggedAnimeGenre, TaggedCharacterType, Video, AnimeGenreTag, ThemeTag
from ..views import anime_series, search_for_anime
from django.urls import reverse
from taggit.managers import TaggableManager

class AnimeSeriesTestCase(TestCase):
    def setUp(self):
        num_of_series = 10
        num_of_chapters = 3
        services = ["cda", "gdrive"]
        subbed = True
        title = "randomtitle"

        for serie_number in range(num_of_series):
            anime_serie = AnimeSerie.objects.create(title=f"anime {serie_number}")
            for chapter_number in range(num_of_chapters):
                anime_chapter = AnimeChapter.objects.create(chapter_number=chapter_number, 
                                            subbed=subbed,
                                            anime_serie=anime_serie,
                                            title=title)
                for service in services:
                    Video.objects.create(service=service, video_link="www.localhost.com", anime_chapter=anime_chapter)
    
    def test_is_rendering(self):
        #self.assertEqual(statusCODE201, anime_series(request))
        pass


class AnimeSearchTestCase(TestCase):
    def setUp(self):
        anime_genre_tags = ['Action', 'Adventure', 'Romance', 'Comedy']
        for tag in anime_genre_tags:
            AnimeGenreTag.objects.create(name=tag)
        season = AnimeSerie.SEASONS[1][1]
        status = AnimeSerie.STATUSES[1][1]

        type = AnimeSerie.TYPES[1][1]
        anime_serie_hxh = AnimeSerie.objects.create(title='Hunter x Hunter', status=status, type=type, season=season)
        anime_serie_hxh.anime_genre_tags.add('Action', 'Adventure')
        anime_serie_hxh.character_type_tags.add('Wizards')
        anime_serie_toradora = AnimeSerie.objects.create(title='Toradora!', status=AnimeSerie.STATUSES[2][1], type=AnimeSerie.TYPES[2][1],
                                    season=AnimeSerie.SEASONS[2][1])
        anime_serie_toradora.anime_genre_tags.add('Romance', 'Comedy')
        anime_serie_toradora.character_type_tags.add('human')
        
    def test_genre_search(self):
        anime_series = AnimeSerie.objects.all()
        client=Client()
        url = '{url}?{filter}={value}'.format(
            url=reverse("streamer:search-anime"),
            filter='genre',
            value='Action'
        )
        response = client.get(url)
        self.assertEqual(response.context['anime_series'], anime_series[0])