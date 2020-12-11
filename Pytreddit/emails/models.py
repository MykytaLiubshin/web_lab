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
    from_user = models.IntegerField()
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

class ForumMessage(models.Model):
    to_forum = models.OneToOneField(Forum, on_delete = models.CASCADE)
    contents = models.TextField()
    from_user = models.OneToOneField( Profile , on_delete=models.CASCADE)
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
    contents = models.TextField()
    from_user = models.IntegerField()
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
    to_user = ArrayField(models.CharField(max_length=200))
    subject = models.CharField(max_length=1000, null=True)

