from django.contrib.auth import get_user_model
from django.test import TestCase

from photographic.photos.models import Photo


class UserTest(TestCase):
    def test_photo_has_correct_string(self):
        user_model = get_user_model()

        username = "bob"

        user = user_model.objects.create_user(username, "bob@example.com", "password")
        photo = Photo.objects.create(
            photographer_id=user.id, photo="e120f48d.jpeg", caption="Example photo"
        )

        self.assertEqual(repr(photo), "<Photo: bob e120f48d.jpeg>")
