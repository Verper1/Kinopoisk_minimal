from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from kinopoisk.models import Movie

class MovieModelTest(TestCase):
    def test_create_movie(self):
        movie = Movie.objects.create(
            title="Test",
            description="Desc",
            year_of_publishing=2000,
            rating=8.5,
            genre="horror"
        )

        self.assertEqual(movie.title, "Test")
        self.assertEqual(Movie.objects.count(), 1)

class MainPageTest(TestCase):
    def test_main_page_status(self):
        response = self.client.get(reverse("main_page"))
        self.assertEqual(response.status_code, 200)

class MoviePageTest(TestCase):
    def test_movie_page(self):
        movie = Movie.objects.create(
            title="Test",
            description="Desc",
            year_of_publishing=2000,
            rating=8.0,
            genre="horror"
        )

        url = reverse("movie_page", args=[movie.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

class FilterTest(TestCase):
    def setUp(self):
        Movie.objects.create(
            title="Horror film",
            description="...",
            year_of_publishing=2001,
            rating=8,
            genre="horror"
        )
        Movie.objects.create(
            title="Romance film",
            description="...",
            year_of_publishing=2005,
            rating=7,
            genre="romance"
        )

    def test_genre_filter(self):
        response = self.client.get(reverse("main_page") + "?genre=horror")

        self.assertContains(response, "Horror film")
        self.assertNotContains(response, "Romance film")
