from django.urls import path

from . import views

app_name = "photos"

urlpatterns = [
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/comment/", views.CreateCommentView.as_view(), name="create_comment"),
    path("create/", views.create_photo, name="create"),
]
