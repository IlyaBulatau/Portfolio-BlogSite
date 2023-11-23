from django.db import models
from apps.users.models import User
from phonenumber_field.modelfields import PhoneNumberField

from .validators import GitHubURLValidator, LinkedInURLValidator, TelegramURLValidator


class Contact(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        related_name="contacts",
        blank=False,
        null=False,
        )
    github = models.URLField(blank=True, null=False, validators=[GitHubURLValidator])
    telegram = models.URLField(blank=True, null=False, validators=[TelegramURLValidator])
    linkedin = models.URLField(blank=True, null=False, validators=[LinkedInURLValidator])
    phone = PhoneNumberField(blank=True, null=False)

