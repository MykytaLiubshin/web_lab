from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField

from users.models import Profile
fs = FileSystemStorage(location="/media/photos")


class Forum(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(storage=fs, null=True)
    description = models.TextField()


class Letter(models.Model):
    contents = models.TextField()

    reply_to = models.OneToOneField(
        "self", blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    contents_files = ArrayField(
        models.FileField(blank=True, null=True, storage=fs),
        blank=True,
        default=list,
    )

class Email(models.Model):
    to_user = models.ManyToManyField(Profile, blank=True)
    subject = models.CharField(max_length=1000)

class ForumMessage(models.Model):
    to_forum = models.ManyToManyField(Forum, blank=True, default=list)
    contents = models.TextField()
    contents_files = ArrayField(
        models.FileField(blank=True, null=True, storage=fs),
        blank=True,
        default=list,
    )
