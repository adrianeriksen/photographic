import os

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .utils import generate_example_image
from ..forms import PhotoForm
from ..models import Photo


class PhotoFormTest(TestCase):
    def test_create_photo_with_caption(self):
        image = generate_example_image()
        user = get_user_model().objects.create_user("bob")

        data = {
            "caption": "This is an example photo"
        }
        files = {
            "photo": SimpleUploadedFile("example.jpeg", image.read(), content_type="image/jpeg")
        }

        form = PhotoForm(data, files)

        self.assertTrue(form.is_valid())

        _id = form.create_photo(user)
        photo = Photo.objects.get(pk=_id)

        self.assertEqual(photo.comment_set.count(), 1)

        # Clean up temporary image
        os.remove(photo.photo.path)

    def test_create_photo_with_empty_caption(self):
        image = generate_example_image()
        user = get_user_model().objects.create_user("bob")

        data = {
            "caption": ""
        }
        files = {
            "photo": SimpleUploadedFile("example.jpeg", image.read(), content_type="image/jpeg")
        }

        form = PhotoForm(data, files)

        self.assertTrue(form.is_valid())

        _id = form.create_photo(user)
        photo = Photo.objects.get(pk=_id)

        self.assertEqual(photo.comment_set.count(), 0)

        # Clean up temporary image
        os.remove(photo.photo.path)
