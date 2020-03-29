from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    age = models.IntegerField(default=30, validators=[MinValueValidator(0), MaxValueValidator(200)])
    profile = models.CharField(default='', max_length=150)
    followings = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followers", blank=True)
