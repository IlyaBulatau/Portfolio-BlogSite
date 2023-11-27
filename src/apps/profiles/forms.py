from typing import Any
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory
from phonenumber_field.formfields import PhoneNumberField

from apps.users.constants import USERNAME_LENGTH_MAX, USERNAME_LENGTH_MIN
from apps.users.models import User
from .models import SocialNetwork
from .validators import SocialNetworkValidator


class UserUpdateForm(forms.ModelForm):
   
    username = forms.CharField(
        label=_("Username"),
        max_length=USERNAME_LENGTH_MAX,
        min_length=USERNAME_LENGTH_MIN,
        required=True,
        )
    phone = PhoneNumberField(
        label=_("Phone"),
        required=False,
    )
    email = forms.EmailField(validators=[])
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "phone",
            "avatar",
            "about",
            )
    
    def __init__(self, *args, **kwargs):
        obj = kwargs.get("instance")
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs['readonly'] = True
        self.fields["new_network"] = forms.CharField(validators=[SocialNetworkValidator()], required=False)



class SocialNetworkUpdateForm(forms.ModelForm):

    class Meta:
        model = SocialNetwork
        fields = (
            "link",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        self.fields["link"].label = obj.name
        self.fields["link"].widget.attrs["name"] = "link"
        self.fields["link"].validators.append(SocialNetworkValidator())


UserSocialNetworkFormSet = inlineformset_factory(
            User, 
            SocialNetwork,
            extra=0,
            form=SocialNetworkUpdateForm,
    )