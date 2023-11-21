from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from . import forms
from .models import User


class UserSingUpView(CreateView):
    model = User
    template_name = "users/signup.html"
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy("login_view")
    

class UserLogInView(LoginView):
    template_name = "users/login.html"
    authentication_form = forms.UserLogInForm
    redirect_authenticated_user = True
    next_page = reverse_lazy("index:index_view")


class UserLogoutView(LogoutView):
    template_name = "users/logout.html"
    next_page = reverse_lazy("login_view")