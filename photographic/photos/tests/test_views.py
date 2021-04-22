import io
import os

from django.test import TestCase
from django.urls import reverse
from PIL import Image

from photographic.users.models import User
from photographic.photos.models import Photo


class TestCreateView(TestCase):
    def test_create_new_photo_page(self):
        response = self.client.get(reverse("photos:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Photo:")
        self.assertContains(response, "Caption:")
        self.assertContains(response, "Author:")

    def test_submit_new_photo(self):
        user = User.objects.create_user("jonas")

        file = io.BytesIO()
        image = Image.new("RGB", size=(200, 200), color=(12, 75, 51))
        image.save(file, "jpeg")
        file.name = "example.jpeg"
        file.seek(0)

        data = {
            "photo": file,
            "caption": "Example image",
            "author": user.id
        }

        response = self.client.post(reverse("photos:create"), data)
        photo = Photo.objects.filter(author_id=user.id)[0]

        self.assertRedirects(response, reverse("photos:detail", args=(photo.id,)))

        # Clean up temporary image
        os.remove(photo.photo.path)
