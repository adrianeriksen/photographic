from uuid import uuid4

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from .forms import UserCreationForm
from .models import User, Profile


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["photo_list"] = context["user"].photo_set.order_by("-created_on")
        context["profile"] = context["user"].profile
        return context


class SignUpView(generic.FormView):
    template_name = "users/signup.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Profile
    fields = ("bio", "photo")
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user.id)

    def form_valid(self, form):
        if "photo" in form.changed_data:
            form.instance.photo.name = "profile-photos/" + str(uuid4()) + ".jpg"
        return super().form_valid(form)
