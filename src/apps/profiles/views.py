from typing import Any
from django.db import models
from django.views.generic import DetailView
from apps.users.models import User


class ProfileDetailView(DetailView):
    model = User
    template_name = "profiles/profile.html"
    