from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .forms import PhotoForm
from .models import Photo


class ListView(generic.ListView):
    def get_queryset(self):
        return Photo.objects.order_by("-created_on")[:6]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Photo


@login_required
def create_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.photo.name = str(uuid4()) + ".jpg"
            form.instance.photographer = request.user
            form.save()

            return HttpResponseRedirect(
                reverse("photos:detail", args=(form.instance.id,))
            )
    else:
        form = PhotoForm()

    return render(request, "photos/create.html", {"form": form})
