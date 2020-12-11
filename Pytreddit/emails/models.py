from django.db import models
from django.core.files.storage import FileSystemStorage
from django.contrib.postgres.fields import ArrayField

from users.models import Profile


class Email(models.Model):
    contents = models.TextField()
    from_user = models.CharField(max_length=200)
    reply_to = models.OneToOneField(
        "self", blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    to_user = ArrayField(models.CharField(max_length=200))
    subject = models.CharField(max_length=1000, null=True)

