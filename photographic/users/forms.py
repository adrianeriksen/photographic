from django.contrib.auth import forms as auth_forms
from django.contrib.auth import get_user_model


class UserChangeForm(auth_forms.UserChangeForm):
    class Meta(auth_forms.UserChangeForm.Meta):
        model = get_user_model()


class UserCreationForm(auth_forms.UserCreationForm):
    class Meta(auth_forms.UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username", "email")
