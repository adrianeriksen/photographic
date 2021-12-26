from io import BytesIO
from PIL import Image

from django.core.files import File


def generate_example_image(size=(200, 200)):
    _bytes = BytesIO()

    im = Image.new("RGB", size=size, color=(12, 75, 51))
    im.save(_bytes, "jpeg")

    _bytes.name = "example.jpeg"
    _bytes.seek(0)

    return _bytes


def generate_example_image_file(size=(200, 200)):
    image = generate_example_image(size)
    return File(image)
