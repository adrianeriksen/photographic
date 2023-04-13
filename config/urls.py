from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from photographic.pages.views import CookiePolicy, PrivacyPolicy, Up
from photographic.photos.views import ListView as HomeView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("settings/", include("photographic.settings.urls")),
    path("photos/", include("photographic.photos.urls")),
    path("users/", include("photographic.users.urls")),
    path("cookie-policy/", CookiePolicy.as_view(), name="cookie-policy"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy-policy"),
    path("up/", Up.as_view()),
    path("", HomeView.as_view(), name="home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
