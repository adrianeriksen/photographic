from django.urls import path

from . import views

app_name = "photos"

urlpatterns = [
    path("", views.ListView.as_view(), name="photo_list"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("create/", views.create_photo, name="create"),
]
