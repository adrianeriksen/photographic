from django.urls import path

from . import views

app_name = "photos"

urlpatterns = [
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("create/", views.create_photo, name="create"),
]
