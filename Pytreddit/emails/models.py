from django.db import models
from users.models import Profile
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField

fs = FileSystemStorage(location="/media/photos")


class Forum(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(storage=fs, null=True)
    description = models.TextField()


class Letter(models.Model):
    to_user = models.ManyToManyField(Profile, blank=True)
    subject = models.CharField(max_length=1000)
    contents = models.TextField()
    reply_to = models.OneToOneField(
        "self", blank=True, null=True, on_delete=models.CASCADE
    )
    contents_files = ArrayField(
        models.FileField(blank=True, null=True, storage=fs),
        blank=True,
        default=list,
    )


class ForumMessage(models.Model):
    to_forum = models.ManyToManyField(Forum, blank=True, default=list)
    subject = models.CharField(max_length=1000)
    contents = models.TextField()
    contents_files = ArrayField(
        models.FileField(blank=True, null=True, storage=fs),
        blank=True,
        default=list,
    )
