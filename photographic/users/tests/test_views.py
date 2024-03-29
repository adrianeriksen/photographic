from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.test import RequestFactory, TestCase

from photographic.users.models import User
from photographic.users.views import DetailView


class TestDetailView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_authentication(self):
        username = "jonas"
        user = User.objects.create_user("jonas")

        request = self.rf.get("/example/path")
        request.user = user

        response = DetailView.as_view()(request, slug=username)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"<h1>{username}</h1>")

    def test_no_authentication(self):
        user = User.objects.create_user("jonas")

        request = self.rf.get("/example/path")
        request.user = AnonymousUser()

        response = DetailView.as_view()(request, slug=user.username)
        login_url = settings.LOGIN_URL + "?next=/example/path"

        self.assertRedirects(response, login_url, fetch_redirect_response=False)


class TestLoginView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_redirects_to_correct_path(self):
        next_page = "/example/path/"
        endpoint = "/accounts/login/?next=" + next_page

        request = self.rf.get(endpoint)
        request.user = AnonymousUser()

        response = LoginView.as_view()(request)

        expected_form_action = f'action="{endpoint}"'

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, expected_form_action)
