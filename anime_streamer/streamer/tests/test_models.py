from django.test import TestCase
from ..models import AnimeSerie, AnimeChapter, Video

class AnimeSerielTestCase(TestCase):
    def setUp(self):
        self.title = "Naruto"
        self.naruto = AnimeSerie.objects.create(title=self.title)

    def test_str(self):
        self.assertEqual(f"{self.title}", str(self.naruto))
    def test_get_absolute_url(self):
        self.assertEqual(f'/animes/{self.title}/', self.naruto.get_absolute_url())

class AnimeChapterTestCase(TestCase):
    def setUp(self):
        self.title = "Naruto"
        self.chapter_number = 3
        self.chapter_title = "example title"
        self.subbed = True

        self.naruto = AnimeSerie.objects.create(title=self.title)
        self.naruto_ch_1 = AnimeChapter.objects.create(anime_serie=self.naruto, chapter_number = self.chapter_number,title=self.chapter_title, subbed=self.subbed)


    def test_str(self):
        self.assertEqual(f"{self.naruto_ch_1}", f"{self.title} {self.chapter_number} {self.chapter_title}")
    def test_get_absolute_url(self):
        self.assertEqual(f'/animes/{self.title}/{self.chapter_number}/', self.naruto_ch_1.get_absolute_url())

class VideoTestCase(TestCase):
    def setUp(self):
        self.title = "Naruto"
        self.chapter_number = 3
        self.chapter_title = "example title"
        self.subbed = True
        self.video_link = "www.examplevideolink.com"
        self.service = "CDA"

        self.naruto = AnimeSerie.objects.create(title=self.title)
        self.naruto_ch_1 = AnimeChapter.objects.create(anime_serie=self.naruto, chapter_number = self.chapter_number,title=self.chapter_title, subbed=self.subbed)
        self.naruto_ch_cda = Video.objects.create(service = self.service, video_link=self.video_link, anime_chapter=self.naruto_ch_1)

    def test_str(self):
            self.assertEqual(f"{self.naruto_ch_cda}", f"{self.title} {self.chapter_number} {self.chapter_title} {self.service}")
