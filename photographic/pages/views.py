from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView


class CookiePolicy(TemplateView):
    template_name = "pages/cookie_policy.html"


class PrivacyPolicy(TemplateView):
    template_name = "pages/privacy_policy.html"


class Up(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Cleared for takeoff!')
