from uuid import uuid4

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import PhotoForm
from .models import Photo


class DetailView(generic.DetailView):
    model = Photo


def create_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.photo.name = str(uuid4()) + ".jpg"
            form.save()

            return HttpResponseRedirect(reverse("photos:detail", args=(form.instance.id,)))
    else:
        form = PhotoForm()

    return render(request, "photos/create.html", {"form": form})
