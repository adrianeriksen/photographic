from django.views.generic import TemplateView


class CookiePolicy(TemplateView):
    template_name = "pages/cookie_policy.html"


class PrivacyPolicy(TemplateView):
    template_name = "pages/privacy_policy.html"
