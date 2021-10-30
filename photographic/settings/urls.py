from django.urls import path

from . import views

app_name = "settings"

urlpatterns = [
    path("profile/", views.UpdateProfileView.as_view(), name="profile"),
    path("password/", views.UpdatePasswordView.as_view(), name="password"),
]
