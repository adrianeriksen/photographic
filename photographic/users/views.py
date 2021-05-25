from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .models import User


class ListView(generic.ListView):
    model = User


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    slug_field = "username"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["photo_list"] = context["user"].photo_set.all()
        return context
