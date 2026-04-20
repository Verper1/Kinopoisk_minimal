from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.core.exceptions import ValidationError


def validate_year(value: int) -> None:
    """Проверяет, что год выпуска фильма находится в допустимом диапазоне."""
    current_year = date.today().year

    if value < 1700:
        raise ValidationError("Год не может быть меньше 1700")

    if value > current_year:
        raise ValidationError(f"Год не может быть больше {current_year}")


class Movie(models.Model):
    GENRE_CHOICES = [
        ("horror", "Ужас"),
        ("romance", "Романтика"),
        ("fantasy", "Фэнтези"),
        ("documentary", "Документальный"),
    ]

    class Meta:
        """Особые настройки."""

        ordering = ["-rating"]
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    cover = models.ImageField(verbose_name="Обложка", upload_to="images/")
    title = models.CharField(verbose_name="Название", max_length=100)
    description = models.CharField(verbose_name="Описание", max_length=1000)
    year_of_publishing = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска", validators=[validate_year]
    )
    rating = models.DecimalField(
        verbose_name="Рейтинг",
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(10.0),
        ],
    )
    genre = models.CharField(verbose_name="Жанр", choices=GENRE_CHOICES, max_length=20)
