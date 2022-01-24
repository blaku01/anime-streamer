from django.test import TestCase
from ..models import AnimeSerie, AnimeChapter, Video

class AnimeSerielTestCase(TestCase):
    def setUp(self):
        self.title = "Naruto"
        self.naruto = AnimeSerie.objects.create(title=self.title)

    def test_str(self):
        self.assertEqual(f"{self.title}", str(self.naruto))
    def test_get_absolute_url(self):
        self.assertEqual(f'/{self.title.lower()}/', self.naruto.get_absolute_url())
