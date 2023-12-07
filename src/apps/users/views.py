from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from allauth.socialaccount.models import SocialApp

from .mixins import LoginPermissionMixin
from . import forms
from .models import User


class UserSingUpView(CreateView):
    model = User
    extra_context = {"social": SocialApp.objects.all()}
    template_name = "users/signup.html"
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("users:login_view")


class UserLogInView(LoginView):
    template_name = "users/login.html"
    extra_context = {"social": SocialApp.objects.all()}
    authentication_form = forms.UserLogInForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("core:index_view")


class UserLogoutView(LoginPermissionMixin, LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("users:login_view")
