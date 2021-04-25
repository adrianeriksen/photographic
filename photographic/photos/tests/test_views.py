import io
import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse
from PIL import Image

from photographic.users.models import User
from photographic.photos.models import Photo
from photographic.photos.views import DetailView


class TestDetailView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_authentication(self):
        user = User.objects.create_user("bob")
        photo = Photo.objects.create(author_id=user.id, photo="e120f48d.jpeg", caption="Example photo")

        request = self.rf.get("/p/1")
        request.user = user

        response = DetailView.as_view()(request, pk=photo.id)

        self.assertEqual(response.status_code, 200)

    def test_no_authentication(self):
        user = User.objects.create_user("bob")
        photo = Photo.objects.create(author_id=user.id, photo="e120f48d.jpeg", caption="Example photo")

        request = self.rf.get("/p/1")
        request.user = AnonymousUser()

        response = DetailView.as_view()(request, pk=photo.id)
        login_url = settings.LOGIN_URL + "?next=/p/1"

        self.assertRedirects(response, login_url, fetch_redirect_response=False)


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

        self.assertRedirects(response, reverse("photos:detail", args=(photo.id,)), fetch_redirect_response=False)

        # Clean up temporary image
        os.remove(photo.photo.path)
