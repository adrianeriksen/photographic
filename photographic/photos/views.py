from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .forms import PhotoForm
from .models import Comment, Photo
from .utils import crop_image


class ListView(generic.ListView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Photo.objects.order_by("-created_on")[:6]

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

    photo_id = None

    def form_valid(self, form):
        cropped_photo = crop_image(form.cleaned_data["photo"])
        current_user = self.request.user

        photo = Photo.objects.create(
            photo=cropped_photo,
            photographer=current_user
        )

        Comment.objects.create(
            content=form.cleaned_data["caption"],
            photo=photo,
            author=current_user
        )

        self.photo_id = photo.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("photos:detail", args=(self.photo_id,))
