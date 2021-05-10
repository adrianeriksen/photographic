from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.views import LoginView
from django.test import RequestFactory, TestCase
from django.urls import reverse

from photographic.users.models import User


class TestIndexView(TestCase):
    def test_user_list_view(self):
        User.objects.create_user("jonas")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/u/jonas/">jonas</a>')


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
