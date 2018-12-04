from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now as timezone_now
import os

# Create your models here.
class Author(models.Model):
    name = models.TextField(max_length=100, blank=False, null=False)
    path = models.TextField(max_length=100, blank=False, null=False)
    user_id = models.IntegerField(default=-1)


def upload_to(instance, filename):
    now = timezone_now()
    filename_base, filename_ext = os.path.splitext(filename)
    return 'my_uploads/{}_{}{}'.format(
        now.strftime("%Y_%m_%d/%H%M%S"),
        filename_base,
        filename_ext.lower()
    )


class Attachment(models.Model):
    parent_id = models.CharField(max_length=18)
    file_name = models.CharField(max_length=255)
    attachment = models.FileField(upload_to=upload_to)
    user_id = models.IntegerField(default=-1)

    def __str__(self):
        return self.file_name

    class Meta:
        ordering = ["-file_name"]


class Html(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100, default="", blank=False, null=False)
    attachment = models.ForeignKey(Attachment, on_delete=models.CASCADE)
    size = models.IntegerField(default=0)
