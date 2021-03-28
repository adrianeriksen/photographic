from django.test import TestCase
from django.urls import reverse


class TestIndexView(TestCase):
    def test_photo_list_without_photos(self):
        response = self.client.get(reverse("photos:photo_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sorry, no photos are available.")


class TestCreateView(TestCase):
    def test_create_new_photo_page(self):
        response = self.client.get(reverse("photos:create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Image URL:")
        self.assertContains(response, "Caption:")
        self.assertContains(response, "Author:")
