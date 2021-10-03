from uuid import uuid4

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .forms import PhotoForm
from .models import Comment, Photo


class ListView(generic.ListView):
    def get_queryset(self):
        return Photo.objects.order_by("-created_on")[:6]


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Photo


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
            form.instance.photo.name = str(uuid4()) + ".jpg"
            form.instance.photographer = request.user
            form.save()

            return HttpResponseRedirect(
                reverse("photos:detail", args=(form.instance.id,))
            )
    else:
        form = PhotoForm()

    return render(request, "photos/create.html", {"form": form})
