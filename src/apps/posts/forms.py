from django import forms
from django.core.validators import MinLengthValidator
from ckeditor.fields import RichTextFormField

from . import constants as cons
from .models import Post


class PostUpdateForm(forms.ModelForm):
    content = RichTextFormField(required=True, validators=[MinLengthValidator(cons.CONTENT_LENGTH_MIN)])
    is_show = forms.BooleanField(required=False)

    class Meta:
        model = Post
        fields = (
            "content",
            "is_show"
        )