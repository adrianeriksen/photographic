from django.shortcuts import render

from .models import Photo


def photo_list(request):
    photos = Photo.objects.order_by("-created_on")[:9]
    context = {
        "photos": photos
    }
    return render(request, "photos/photo_list.html", context)