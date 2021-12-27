from django import forms


class PhotoForm(forms.Form):
    photo = forms.ImageField()
    caption = forms.CharField(
        widget=forms.Textarea
    )
