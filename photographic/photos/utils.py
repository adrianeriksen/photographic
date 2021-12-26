from io import BytesIO
from PIL import Image
from uuid import uuid4

from django.core.files import File

JPEG_IMAGE_QUALITY = 100


def crop_image(image):
    im = Image.open(image)

    (height, width) = (im.height, im.width)
    shortest_side = min(height, width)
    dimensions = (0, 0, shortest_side, shortest_side)
    image_name = _generate_random_file_name()

    im = im.convert("RGB")
    im = im.crop(dimensions)

    _bytes = BytesIO()

    im.save(_bytes, "JPEG", quality=JPEG_IMAGE_QUALITY)

    return File(_bytes, image_name)


def _generate_random_file_name():
    return str(uuid4()) + ".jpg"
