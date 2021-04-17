from django.core.exceptions import ValidationError
from django.test import TestCase

from photographic.users.validators import AlphanumericUsernameValidator


class UsernameValidatorsTest(TestCase):
    def test_alphanumeric_username_validator(self):
        valid_usernames = ["noah", "oliver90", "123sarah"]
        invalid_usernames = [
            "lucas-elijah",
            "harper_",
            "o'conor",
            "إبراهيم",
            "newlinni\n",
        ]

        v = AlphanumericUsernameValidator()

        for username in valid_usernames:
            v(username)

        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                v(username)
