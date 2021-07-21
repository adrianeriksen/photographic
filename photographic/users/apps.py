from django.apps import AppConfig
from django.db.models.signals import post_save


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "photographic.users"

    def ready(self):
        from .models import User
        from .signals import create_user_profile

        post_save.connect(create_user_profile, sender=User)
