from django import forms

from .models import Comment, Photo
from .utils import crop_image


class PhotoForm(forms.Form):
    photo = forms.ImageField()
    caption = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def create_photo(self, photographer):
        photo = Photo.objects.create(
            photo=self._get_processed_photo(),
            photographer=photographer
        )

        if self.cleaned_data["caption"]:
            Comment.objects.create(
                content=self.cleaned_data["caption"],
                photo=photo,
                author=photographer
            )

        return photo.id

    def _get_processed_photo(self):
        return crop_image(self.cleaned_data["photo"])
