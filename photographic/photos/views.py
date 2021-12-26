from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
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

        photo = context["photo"]
        comments = [
            self._generate_comment(photo.caption, photo.photographer, photo.created_on)
        ]

        for comment in photo.comment_set.all():
            comments.append(
                self._generate_comment(comment.content, comment.author, comment.created_on)
            )

        context["comments"] = comments
        return context

    def _generate_comment(self, content, author, created_on):
        return {
            "author": {
                "username": author.username,
                "photo_url": author.profile.photo.url if author.profile.photo else ""
            },
            "content": content,
            "created_on": created_on
        }


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


@login_required
def create_photo(request):
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            form.instance.photo = crop_image(form.instance.photo)
            form.instance.photographer = request.user
            form.save()

            return HttpResponseRedirect(
                reverse("photos:detail", args=(form.instance.id,))
            )
    else:
        form = PhotoForm()

    return render(request, "photos/create.html", {"form": form})
