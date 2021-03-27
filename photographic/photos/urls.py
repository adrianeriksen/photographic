from django.urls import path

from . import views

app_name = "photos"

urlpatterns = [
    path("", views.photo_list, name="photo_list")
]