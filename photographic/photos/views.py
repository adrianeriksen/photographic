from uuid import uuid4

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PhotoForm
from .models import Photo


def photo_list(request):
    photos = Photo.objects.order_by("-created_on")[:9]
    context = {"photos": photos}
    return render(request, "photos/photo_list.html", context)


def create_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.photo.name = str(uuid4()) + ".jpg"
            form.save()

            return HttpResponseRedirect(reverse("photos:photo_list"))
    else:
        form = PhotoForm()

    return render(request, "photos/create.html", {"form": form})
