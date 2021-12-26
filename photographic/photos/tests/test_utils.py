from PIL import Image

from django.core.files import File
from django.test import TestCase

from .utils import generate_example_image

from ..utils import crop_image


class TestCropImage(TestCase):
    def test_landscape_photo_is_cropped(self):
        image = self._generate_image((400, 200))

        cropped_image = crop_image(image)

        with Image.open(cropped_image) as im:
            self.assertEqual(im.width, 200)
            self.assertEqual(im.height, 200)

    def test_portrait_photo_is_cropped(self):
        image = self._generate_image((200, 400))

        cropped_image = crop_image(image)

        with Image.open(cropped_image) as im:
            self.assertEqual(im.width, 200)
            self.assertEqual(im.height, 200)

    def _generate_image(self, size):
        image = generate_example_image(size)
        return File(image)
