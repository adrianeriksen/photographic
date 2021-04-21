from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from photographic.users.views import ListView as HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("p/", include("photographic.photos.urls")),
    path("u/", include("photographic.users.urls")),
    path("", HomeView.as_view(), name="home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
