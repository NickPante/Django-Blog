from django.db import models
from django.conf import settings


# Create your models here.

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT='DF','Draft'
        PUBLISHED='P','Published'
    author=models.ForeignKey(settings.AUTH_USER_MODEL)
    title=models.CharField()
    slug=models.SlugField()
    body=models.TextField()
    publish=models.DateTimeField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(choices=Status.choices,default=Status.DRAFT)