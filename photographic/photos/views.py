from uuid import uuid4

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
        photo_object = request.FILES["photo"]
        caption = request.POST["caption"]
        author = request.POST["author"]

        photo = Photo(photo=photo_object, caption=caption, author=author)
        extension = photo.photo.name.split(".")[-1]
        photo.photo.name = str(uuid4()) + "." + extension
        photo.save()

        if photo.id:
            return HttpResponseRedirect(reverse("photos:photo_list"))

    return render(request, "photos/create.html")
