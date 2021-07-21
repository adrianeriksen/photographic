from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/edit/", views.UpdateProfileView.as_view(), name="profile"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
