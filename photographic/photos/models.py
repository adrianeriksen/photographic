from django.conf import settings
from django.db import models


class Photo(models.Model):
    photo = models.ImageField()
    caption = models.TextField()
    photographer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.photographer.username} {self.photo}"
