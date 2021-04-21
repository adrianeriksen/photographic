from django.test import TestCase
from django.urls import reverse

from photographic.users.models import User


class TestIndexView(TestCase):
    def test_user_list_view(self):
        User.objects.create_user("jonas")

        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<a href="/u/jonas/">jonas</a>')
