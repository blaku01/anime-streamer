from django.test import TestCase
from ..models import AnimeSerie, AnimeChapter, Video
from ..views import anime_series, series_view, chapter_view, video_view

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
    
    def is_rendering(self):
        #self.assertEqual(statusCODE201, anime_series(request))
        pass
    
    