from uuid import uuid4

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse_lazy

from photographic.users.models import Profile


class UpdatePasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = "settings/password_form.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        logout(self.request)
        return HttpResponseRedirect(self.get_success_url())


class UpdateProfileView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Profile
    fields = ("bio", "photo")
    success_url = reverse_lazy("settings:profile")
    template_name = "settings/profile_form.html"

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user.id)

    def form_valid(self, form):
        if "photo" in form.changed_data:
            form.instance.photo.name = str(uuid4()) + ".jpg"
        return super().form_valid(form)
