from typing import Any
from django.db import models
from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.db.models import QuerySet

from apps.users.mixins import LoginPermissionMixin
from .forms import UserUpdateForm, UserSocialNetworkFormSet
from apps.users.models import User
from .models import SocialNetwork
from apps.users.mixins import OwnerPermissionMixin


class ProfileDetailView(LoginPermissionMixin, DetailView):
    model = User
    template_name = "profiles/profile.html"
    context_object_name = "user_obj"

    def get_queryset(self) -> QuerySet:
        user_slug: str = self.kwargs.get(self.slug_field)
        user: User = User.objects.filter(slug=user_slug).prefetch_related("posts", "networks")
        return user


class ProfileUpdateView(LoginPermissionMixin, OwnerPermissionMixin, UpdateView):
    model = User
    template_name = "profiles/profile_update.html"
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        user_slug: str = self.object.slug
        return reverse_lazy("profiles:profile_detail_view", args=(user_slug,))

    def get_context_data(self, **kwargs) -> dict:
        user: User = self.request.user
        context: dict = super().get_context_data(**kwargs)

        if not self.request.POST:
            context["newtorks_form"] = UserSocialNetworkFormSet(
                instance=user, prefix="networks"
            )
        else:
            # if this is post method
            # add data from post request to networks form
            context["newtorks_form"] = UserSocialNetworkFormSet(
                self.request.POST,
                self.request.FILES,
                instance=user,
            )
        form: UserUpdateForm = self.get_form()
        new_network: str = form.data.get("new_network")

        if new_network:
            # create new network for user
            # if it not exists
            SocialNetwork.objects.get_or_create(link=new_network, user=user)

        return context

    def form_valid(self, form) -> HttpResponse:
        """
        Update data from netwworks form in database
        """
        context: dict = self.get_context_data()

        network_form: UserSocialNetworkFormSet = context["newtorks_form"]

        if network_form.is_valid():
            network_form.save()

        return super().form_valid(form)
