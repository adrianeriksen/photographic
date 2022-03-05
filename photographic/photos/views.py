import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import PhotoForm
from .models import Comment, Photo


class ListView(LoginRequiredMixin, generic.ListView):
    def get_queryset(self):
        following = self.request.user.following.all()
        return Photo.objects.filter(photographer__in=following).order_by("-created_on")[:6]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Photo

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["comments"] = context["photo"].comment_set.all()
        return context


class CreateCommentView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    fields = ["content"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["photo_id"] = self.kwargs["pk"]
        return context

    def get_success_url(self):
        photo_id = self.kwargs["pk"]
        return reverse("photos:detail", args=(photo_id,))

    def form_valid(self, form):
        photo = get_object_or_404(Photo, pk=self.kwargs["pk"])

        form.instance.author = self.request.user
        form.instance.photo = photo

        return super().form_valid(form)


class UploadPhotoView(LoginRequiredMixin, generic.FormView):
    form_class = PhotoForm
    template_name = "photos/photo_form.html"

    def form_valid(self, form):
        photo_id = form.create_photo(photographer=self.request.user)
        success_url = reverse("photos:detail", args=(photo_id,))
        return HttpResponseRedirect(success_url)


def _get_random_users():
    users = Photo.objects.values("photographer_id").annotate(num_photos=Count('id'))
    usernames = [user["photographer_id"] for user in users if user["num_photos"] >= 3]
    return random.sample(usernames, k=2) if len(usernames) > 2 else usernames


class DiscoverView(LoginRequiredMixin, generic.ListView):
    queryset = Photo.objects.order_by("-created_on")[:3]
