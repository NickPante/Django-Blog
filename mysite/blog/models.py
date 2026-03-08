from django.db import models
from django.conf import settings
from taggit.managers import TaggableManager
from django.urls import reverse


# Create your models here.


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "P", "Published"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # ΟΤΑΝ ΔΙΑΓΡΑΦΕΤΕ Ο AUTHOR ΔΙΑΓΡΑΦΟΝΤΑΙ ΤΑ POST ΤΟΥ
    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date="publish"
    )  # Ο ΤΙΤΛΟΣ ΤΟΥ BLOG
    body = models.TextField()
    publish = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=Status.choices, default=Status.DRAFT)

    tags = TaggableManager()

    def get_absolute_url(self):  # ΔΙΝΕΙ ΤΑ ΕΞΗς ΔΕΔΟΜΕΝΑ ΣΤΟ ΜΟΝΑΔΙΚΟ URL ΠΟΥ ΦΤΟΙΑΧΝΕΙ
        return reverse(
            "blog:post_detail",
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
        )


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["created"]  # ΤΑΞΙΝΟΜΕΙ ΤΑ ΣΧΟΛΕΙΑ
