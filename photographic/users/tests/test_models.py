from django.db.utils import DataError
from django.test import TestCase

from photographic.users.models import Profile, User


class ProfileModelTests(TestCase):
    def test_profile_is_created_with_user(self):
        username = "alice"
        user = User.objects.create_user(username)

        profile_count = Profile.objects.filter(user_id=user.id).count()

        self.assertEqual(profile_count, 1, "Number of profiles other than 1")


class UserModelTests(TestCase):
    def test_full_name_returns_username(self):
        username = "alice"
        user = User.objects.create_user(username)
        self.assertEqual(
            user.get_full_name(), username, "Full name differ from username"
        )

    def test_short_name_returns_username(self):
        username = "bob"
        user = User.objects.create_user(username)
        self.assertEqual(
            user.get_short_name(), username, "Short name differ from username"
        )

    def test_long_username_not_allowed(self):
        username = "x" * 31

        with self.assertRaises(DataError, msg="User with too long username created"):
            User.objects.create_user(username)

    def test_username_with_max_length(self):
        username = "x" * 30
        user = User.objects.create_user(username)
        self.assertEqual(user.username, username)

    def test_usernames_tranformed_to_lowercase(self):
        username = "ADRIAN"

        u = User(username=username, password="password", email="adrian@example.com")
        u.full_clean()

        self.assertEqual(u.username, username.lower())
