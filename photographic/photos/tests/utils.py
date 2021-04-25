import io

from PIL import Image


def generate_example_image():
    file = io.BytesIO()
    image = Image.new("RGB", size=(200, 200), color=(12, 75, 51))
    image.save(file, "jpeg")
    file.name = "example.jpeg"
    file.seek(0)

    return file
