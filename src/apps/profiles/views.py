from django.http import HttpResponse
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import UserUpdateForm, UserSocialNetworkFormSet
from apps.users.models import User
from .models import SocialNetwork
from apps.users.mixins import UpdatePermissionMixin


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profiles/profile.html"
    context_object_name = "user_obj"


class ProfileUpdateView(LoginRequiredMixin, UpdatePermissionMixin, UpdateView):
    model = User
    template_name = "profiles/profile_update.html"
    form_class = UserUpdateForm

    def get_success_url(self) -> str:
        user_slug = self.object.slug
        return reverse_lazy("profiles:profile_detail_view", args=(user_slug,))

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if not self.request.POST:
            context["newtorks_form"] = UserSocialNetworkFormSet(
                instance=user, prefix="networks"
            )
        else:
            context["newtorks_form"] = UserSocialNetworkFormSet(
                self.request.POST,
                self.request.FILES,
                instance=user,
            )
        form = self.get_form()
        new_network = form.data.get("new_network")
        if new_network:
            SocialNetwork.objects.filter(link=new_network, user=user).get_or_create(
                link=new_network, user=user
            )

        return context

    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()

        network_form = context["newtorks_form"]

        if network_form.is_valid():
            network_form.save()

        return super().form_valid(form)
