from django.contrib.auth.models import UserManager
from django.test import TestCase

from photographic.users.models import User


class UserModelTests(TestCase):
    def test_full_name_returns_username(self):
        username = "alice"
        user = User.objects.create_user(username, "alice@example.com", "password")
        self.assertEqual(
            user.get_full_name(), username, "Full name differ from username"
        )

    def test_short_name_returns_username(self):
        username = "bob"
        user = User.objects.create_user(username, "bob@example.com", "password")
        self.assertEqual(
            user.get_short_name(), username, "Short name differ from username"
        )
