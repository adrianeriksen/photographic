from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
