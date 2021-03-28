from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Photo


def photo_list(request):
    photos = Photo.objects.order_by("-created_on")[:9]
    context = {"photos": photos}
    return render(request, "photos/photo_list.html", context)


def create_photo(request):
    if request.method == "POST":
        image_url = request.POST["image-url"]
        caption = request.POST["caption"]
        author = request.POST["author"]

        photo = Photo(photo=image_url, caption=caption, author=author)
        photo.save()

        if photo.id:
            return HttpResponseRedirect(reverse("photos:photo_list"))

    return render(request, "photos/create.html")
