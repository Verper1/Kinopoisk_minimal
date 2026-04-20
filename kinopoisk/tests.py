import io

import pytest
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from django.urls import reverse

from kinopoisk.models import Movie


def _png_upload() -> SimpleUploadedFile:
    """Создаёт валидный PNG в памяти для загрузки в форму."""
    buffer = io.BytesIO()
    Image.new("RGB", (1, 1), color="red").save(buffer, format="PNG")
    return SimpleUploadedFile("cover.png", buffer.getvalue(), content_type="image/png")


@pytest.fixture
def client() -> Client:
    """Тестовый клиент Django."""
    return Client()


@pytest.fixture
def horror_movie() -> Movie:
    """Фильм ужасов."""
    return Movie.objects.create(
        title="Horror film",
        description="scary story",
        year_of_publishing=2001,
        rating=8,
        genre="horror",
    )


@pytest.fixture
def romance_movie() -> Movie:
    """Романтический фильм."""
    return Movie.objects.create(
        title="Romance film",
        description="love story",
        year_of_publishing=2005,
        rating=7,
        genre="romance",
    )


@pytest.mark.django_db
def test__add_movie_view__add_movie(client: Client) -> None:
    """Тест добавления фильма через POST на add_movie."""
    response = client.post(
        reverse("add_movie"),
        data={
            "title": "New film",
            "description": "desc",
            "year_of_publishing": 2010,
            "rating": "7.5",
            "genre": "fantasy",
            "cover": _png_upload(),
        },
    )

    assert response.status_code == 302
    assert response.url == reverse("main_page")
    assert Movie.objects.filter(title="New film").count() == 1


@pytest.mark.django_db
def test__show_movie_page_view__movie_page_404(client: Client) -> None:
    """404 для несуществующего фильма."""
    response = client.get(reverse("movie_page", args=[9999]))

    assert response.status_code == 404


@pytest.mark.django_db
def test__main_page_view__search_by_title(
    client: Client, horror_movie: Movie, romance_movie: Movie
) -> None:
    """Поиск по названию."""
    response = client.get(reverse("main_page"), {"search": "Horror"})

    assert response.status_code == 200
    assert b"Horror film" in response.content
    assert b"Romance film" not in response.content


@pytest.mark.django_db
def test__main_page_view__search_by_description(
    client: Client, horror_movie: Movie, romance_movie: Movie
) -> None:
    """Поиск по описанию."""
    response = client.get(reverse("main_page"), {"search": "love"})

    assert response.status_code == 200
    assert b"Romance film" in response.content
    assert b"Horror film" not in response.content


@pytest.mark.django_db
def test__main_page_view__combined_filters(
    client: Client, horror_movie: Movie, romance_movie: Movie
) -> None:
    """Комбинированные фильтры: жанр + мин. рейтинг + год."""
    response = client.get(
        reverse("main_page"),
        {"genre": "horror", "min_rating": "7.5", "year_of_publishing": 2001},
    )

    assert response.status_code == 200
    assert b"Horror film" in response.content
    assert b"Romance film" not in response.content


@pytest.mark.django_db
def test__main_page_view__combined_filters_no_match(
    client: Client, horror_movie: Movie, romance_movie: Movie
) -> None:
    """Комбинированные фильтры без совпадений возвращают пустой список."""
    response = client.get(
        reverse("main_page"),
        {"genre": "horror", "min_rating": "9"},
    )

    assert response.status_code == 200
    assert b"Horror film" not in response.content
    assert b"Romance film" not in response.content


@pytest.mark.django_db
def test__main_page_view__invalid_query_params(
    client: Client, horror_movie: Movie, romance_movie: Movie
) -> None:
    """Невалидные query-параметры не роняют страницу, форма помечается как невалидная."""
    response = client.get(
        reverse("main_page"),
        {"min_rating": "abc", "year_of_publishing": "not-a-year"},
    )

    assert response.status_code == 200
    form = response.context["form"]
    assert not form.is_valid()
    assert "min_rating" in form.errors
    assert "year_of_publishing" in form.errors
