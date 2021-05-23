import os

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from django.urls import reverse

from photographic.users.models import User
from photographic.photos.models import Photo
from photographic.photos.views import DetailView, create_photo
from .utils import generate_example_image


class TestDetailView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_authentication(self):
        user = User.objects.create_user("bob")
        photo = Photo.objects.create(
            photographer_id=user.id, photo="e120f48d.jpeg", caption="Example photo"
        )

        request = self.rf.get("/p/1")
        request.user = user

        response = DetailView.as_view()(request, pk=photo.id)

        self.assertEqual(response.status_code, 200)

    def test_no_authentication(self):
        user = User.objects.create_user("bob")
        photo = Photo.objects.create(
            photographer_id=user.id, photo="e120f48d.jpeg", caption="Example photo"
        )

        request = self.rf.get("/p/1")
        request.user = AnonymousUser()

        response = DetailView.as_view()(request, pk=photo.id)
        login_url = settings.LOGIN_URL + "?next=/p/1"

        self.assertRedirects(response, login_url, fetch_redirect_response=False)


class TestCreateView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_no_authentication(self):
        path = reverse("photos:create")
        request = self.rf.get(path)
        request.user = AnonymousUser()

        response = create_photo(request)
        login_url = settings.LOGIN_URL + "?next=" + path

        self.assertRedirects(response, login_url, fetch_redirect_response=False)

    def test_form_shows_when_authenticated(self):
        user = User.objects.create_user("bob")

        request = self.rf.get("/example/path")
        request.user = user

        response = create_photo(request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Photo:")
        self.assertContains(response, "Caption:")
        self.assertNotContains(response, "Author:")

    def test_submit_new_photo(self):
        user = User.objects.create_user("jonas")

        data = {
            "photo": generate_example_image(),
            "caption": "Example image",
        }

        request = self.rf.post("/example/path", data)
        request.user = user

        response = create_photo(request)
        photo = Photo.objects.filter(photographer_id=user.id)[0]

        self.assertRedirects(
            response,
            reverse("photos:detail", args=(photo.id,)),
            fetch_redirect_response=False,
        )

        # Clean up temporary image
        os.remove(photo.photo.path)
