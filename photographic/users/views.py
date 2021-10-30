from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse, reverse_lazy

from .forms import UserCreationForm
from .models import User


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["photo_list"] = context["user"].photo_set.order_by("-created_on")
        context["profile"] = context["user"].profile
        context["is_following"] = self.request.user == context["user"] or self.request.user in context["user"].followers.all()
        return context


class FollowUserView(LoginRequiredMixin, generic.RedirectView):
    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs["slug"])
        if user.id != request.user.id:
            user.followers.add(request.user)
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        username = self.kwargs["slug"]
        return reverse("users:detail", args=(username,))


class SignUpView(generic.FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
