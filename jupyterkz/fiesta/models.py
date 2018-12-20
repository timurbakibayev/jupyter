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
    user = User.objects.get(pk=instance.parent_id)
    filename_base, filename_ext = os.path.splitext(filename)
    return '{}/{}_{}{}'.format(user.username.replace(" ","").lower(),
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
    date_time = models.DateTimeField(auto_now_add=True)
    size = models.IntegerField(default=0)
    visits = models.IntegerField(default=0)

    def calc_size(self):
        try:
            return self.attachment.attachment.size //1024
        except:
            return "0"


class Visit(models.Model):
    url = models.TextField(max_length=1000, default="", blank=False, null=False)
    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.date_time) + " " + self.url
