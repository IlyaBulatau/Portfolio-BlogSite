from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.views.generic import DetailView, UpdateView
from django.urls import reverse_lazy

from .forms import UserUpdateForm, UserSocialNetworkFormSet
from apps.users.models import User


class ProfileDetailView(DetailView):
    model = User
    template_name = "profiles/profile.html"


class ProfileUpdateView(UpdateView):
    model = User
    template_name = "profiles/profile_update.html"
    form_class = UserUpdateForm


    def get_success_url(self) -> str:
        user_slug = self.request.user.slug
        return reverse_lazy("profiles:profile_detail_view", args=(user_slug, ))


    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)

        if not self.request.POST:        
            context["newtorks_form"] = UserSocialNetworkFormSet(instance=user, prefix="networks")
        else:
            context["newtorks_form"] = UserSocialNetworkFormSet(
                                        self.request.POST,
                                        self.request.FILES,
                                        instance=user,
                                        )
        return context



    def form_valid(self, form) -> HttpResponse:
        context = self.get_context_data()

        network_form = context["newtorks_form"]
        
        if network_form.is_valid():
            network_form.save()
        
        return super().form_valid(form)
