from django.db import models


class Photo(models.Model):
    photo = models.URLField("Photo URL")
    caption = models.TextField()
    author = models.CharField(max_length=30)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.author
