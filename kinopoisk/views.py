from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpRequest, HttpResponse


from kinopoisk.models import Movie
from .forms import MovieForm


def main_page_view(request: HttpRequest) -> HttpResponse:
    """
    View, которая возвращает страницу с всеми фильмами или предлагает добавить фильм.
    На странице есть поисковик по названию или описанию и поиск по фильтрам.
    """
    movies = Movie.objects.all()

    search = request.GET.get("search")
    if search:
        movies = movies.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    genre = request.GET.get("genre")
    if genre:
        movies = movies.filter(genre__iexact=genre)

    min_rating = request.GET.get("min_rating")
    if min_rating:
        movies = movies.filter(rating__gte=min_rating)

    year_of_publishing = request.GET.get("year_of_publishing")
    if year_of_publishing:
        movies = movies.filter(year_of_publishing=year_of_publishing)

    return render(request, "index.html", {"movies": movies})


def add_movie_view(request: HttpRequest) -> HttpResponse:
    """
    View для добавления фильма в базу.
    """
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("main_page")
    else:
        form = MovieForm()

    return render(request, "add_movie.html", {"form": form})


def show_movie_page_view(request: HttpRequest, movie_id: int) -> HttpResponse:
    """
    View для показа информации о фильме или выбрасывание 404 ошибки при отсутствии фильма в базе.
    """
    movie = get_object_or_404(Movie, pk=movie_id)

    return render(request, "movie_page.html", {"movie": movie})
