from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import AlphanumericUsernameValidator


class User(AbstractUser):
    """
    An implementation of a user model with admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = AlphanumericUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text=_('Required. 30 characters or fewer. Letters and digits.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = None
    last_name = None

    def clean(self):
        super().clean()
        setattr(self, self.USERNAME_FIELD, self.get_username().lower())

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username