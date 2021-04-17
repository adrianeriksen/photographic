from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("<slug:slug>/", views.DetailView.as_view(), name="detail"),
]
