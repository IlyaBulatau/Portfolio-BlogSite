from typing import Any
from django.db import models
from django.views.generic import DetailView, UpdateView
from apps.users.models import User


class ProfileDetailView(DetailView):
    model = User
    template_name = "profiles/profile.html"


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "profiles/profile_update.html"
    fields = ("username", )