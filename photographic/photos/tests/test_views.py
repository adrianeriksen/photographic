from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_photo_list_without_photos(self):
        response = self.client.get(reverse("photos:photo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no photos are available.")
