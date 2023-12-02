from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _

from . import constants as cons
from .models import User


class UserSignUpForm(UserCreationForm):
    username = forms.CharField(
        label=_("Username"),
        max_length=cons.USERNAME_LENGTH_MAX,
        min_length=cons.USERNAME_LENGTH_MIN,
    )
    email = forms.EmailField(label=_("Email"))

    class Meta:
        model = User
        fields = ["username", "email"]


class UserLogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email"]
