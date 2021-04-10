from django.db.utils import DataError
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

    def test_long_username_not_allowed(self):
        username = "x" * 31

        with self.assertRaises(DataError, msg="User with too long username created"):
            User.objects.create_user(username, "bob@example.com", "password")

    def test_username_with_max_length(self):
        username = "x" * 30
        user = User.objects.create_user(username, "bob@example.com", "password")
        self.assertEqual(user.username, username)
