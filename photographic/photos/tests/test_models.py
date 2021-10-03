from django.contrib.auth import get_user_model
from django.test import TestCase

from photographic.photos.models import Comment, Photo


class CommentTest(TestCase):
    def test_comment_has_correct_string(self):
        user_model = get_user_model()

        username = "bob"
        photo_name = "e120f48d.jpeg"

        user = user_model.objects.create_user(username, "bob@example.com", "password")
        photo = Photo.objects.create(
            photographer_id=user.id, photo=photo_name, caption="Example photo"
        )
        comment = Comment.objects.create(content="Lorem ipsum", photo_id=photo.id, author_id=user.id)

        self.assertEqual(repr(comment), f"<Comment: {comment.created_on} {username} on {photo_name}>")


class UserTest(TestCase):
    def test_photo_has_correct_string(self):
        user_model = get_user_model()

        username = "bob"
        photo_name = "e120f48d.jpeg"

        user = user_model.objects.create_user(username, "bob@example.com", "password")
        photo = Photo.objects.create(
            photographer_id=user.id, photo=photo_name, caption="Example photo"
        )

        self.assertEqual(repr(photo), f"<Photo: {photo_name}>")
