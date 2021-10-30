from django.test import RequestFactory, TestCase

from photographic.users.models import Profile, User
from photographic.settings.views import UpdateProfileView


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