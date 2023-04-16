from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.contrib import admin
from django.urls import include, path

from photographic.photos.views import ListView as HomeView


def up(request):
    return HttpResponse("Cleared for takeoff!")


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("settings/", include("photographic.settings.urls")),
    path("photos/", include("photographic.photos.urls")),
    path("users/", include("photographic.users.urls")),
    path("up/", up),
    path("", HomeView.as_view(), name="home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
