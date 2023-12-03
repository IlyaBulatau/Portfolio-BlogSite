from django import forms
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextFormField
from django.utils.translation import gettext_lazy as _

from . import constants as cons
from .models import Post
from .choices import TAGS_CHOISE


class PostUpdateForm(forms.ModelForm):
    content = RichTextFormField(
        required=True, validators=[MinLengthValidator(cons.CONTENT_LENGTH_MIN)]
    )
    is_show = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = ("content", "is_show")


class PostCreateForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        max_length=cons.TITLE_LENGTH_MAX,
        validators=[MinLengthValidator(cons.TITLE_LENGTH_MIN)])
    content = RichTextFormField(
        required=True,
        validators=[MinLengthValidator(cons.CONTENT_LENGTH_MIN)])
    image = forms.ImageField(required=False)
    tag = forms.ChoiceField(choices=TAGS_CHOISE, required=True)

    class Meta:
        model = Post
        fields = (
            "title",
            "content",
            "image",
        )