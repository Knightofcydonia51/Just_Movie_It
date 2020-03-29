from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=150)
    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=150)
    director = models.CharField(max_length=30)

    age = models.IntegerField(default = 0)
    audience = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    poster_url = models.CharField(max_length=300, default="/static/images/noimage2.jpg")
    description = models.TextField(default='')
    movie_score = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movies", blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)


class Review(models.Model):
    content = models.CharField(max_length=150)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)