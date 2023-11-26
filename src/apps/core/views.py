from django.views import generic
from django.contrib.auth.models import User


class HealthcheckView(generic.TemplateView):
    template_name = "index/index.html"
