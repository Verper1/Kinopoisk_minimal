from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        """Особые настройки."""

        model = Movie
        fields = "__all__"
        widgets = {"description": forms.Textarea()}


class MovieFilterForm(forms.Form):
    genre = forms.ChoiceField(
        required=False, label="Жанр", choices=[("", "Любой жанр")] + Movie.GENRE_CHOICES
    )
    min_rating = forms.FloatField(
        required=False,
        label="Мин. рейтинг",
    )
    year_of_publishing = forms.IntegerField(required=False, label="Год")
    search = forms.CharField(
        required=False,
        label="Название или описание",
    )
