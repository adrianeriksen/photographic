from django.conf import settings
from django.db import models


class Photo(models.Model):
    photo = models.ImageField()
    photographer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.photo)


class Comment(models.Model):
    content = models.TextField()
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_on} {self.author.username} on {self.photo.photo}"
