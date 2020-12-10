from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    login = models.CharField(max_length=200, unique=True)
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)

    is_stuff = models.BooleanField(default=False)

    profile_picture_name = models.CharField(max_length=200, blank=True)
    profile_link = models.CharField(max_length=200, blank=True)

    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.username
