from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse_lazy

from photographic.users.models import Profile, User
from photographic.settings.views import UpdatePasswordView, UpdateProfileView


class TestUpdatePasswordView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_user_is_deauthenticated_after_password_change(self):
        pass

    def test_user_is_redirected_to_login_page(self):
        user = User.objects.create_user("adrian", email="adrian@example.com", password="password")

        data = {
            "old_password": "password",
            "new_password1": "securepassword",
            "new_password2": "securepassword"
        }

        request = self.rf.post("/example/path", data)
        request.user = user
        request._dont_enforce_csrf_checks = True

        session_middleware = SessionMiddleware()
        session_middleware.process_request(request)

        request.session.save()

        response = UpdatePasswordView.as_view()(request)

        login_url = reverse_lazy("login")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, login_url)


class TestUpdateProfileView(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_photo_keeps_name_on_update(self):
        photo_file_name = "1b4a9aec.jpeg"
        user = User.objects.create_user("jonas")

        profile = Profile.objects.get(user=user.id)
        profile.photo = photo_file_name
        profile.save()

        request = self.rf.post("/example/path", {})
        request.user = user

        response = UpdateProfileView.as_view()(request)

        self.assertEqual(response.status_code, 302)

        updated_profile = Profile.objects.get(user=user.id)

        self.assertEqual(updated_profile.photo.name, photo_file_name)