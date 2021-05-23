from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from photographic.pages.views import CookiePolicy, PrivacyPolicy
from photographic.users.views import ListView as HomeView

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("admin/", admin.site.urls),
    path("p/", include("photographic.photos.urls")),
    path("u/", include("photographic.users.urls")),
    path("cookie-policy/", CookiePolicy.as_view(), name="cookie-policy"),
    path("privacy-policy/", PrivacyPolicy.as_view(), name="privacy-policy"),
    path("", HomeView.as_view(), name="home")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
