from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import EmailValidator, MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify

from phonenumber_field.modelfields import PhoneNumberField

from . import constants as cons


class User(AbstractUser):
    username_error_message = {
        "unique": _("A user with that username already exists."),
        "don't exists": _("There is no user with this username"),
    }

    username = models.CharField(
        max_length=cons.USERNAME_LENGTH_MAX,
        unique=True,
        help_text=_("Required.")
        + f"{cons.USERNAME_LENGTH_MAX}"
        + _("characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[
            UnicodeUsernameValidator(),
            MinLengthValidator(cons.USERNAME_LENGTH_MIN),
        ],
        error_messages=username_error_message,
        blank=False,
    )
    email = models.EmailField(
        unique=True,
        help_text=_("Enter a valid email address"),
        validators=[EmailValidator()],
        blank=False,
    )
    password = models.CharField(blank=False, max_length=128)
    slug = models.SlugField(
        max_length=cons.SLUG_LENGTH_MAX, blank=False, unique=True, db_index=True
    )
    avatar = models.ImageField(blank=True, upload_to="profile/")
    phone = PhoneNumberField(blank=True, null=False)
    about = models.TextField(blank=True)
    created_on = models.DateTimeField(
        auto_now_add=True,
    )
    update_on = models.DateTimeField(
        auto_now=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return f"{self.pk} | {self.username}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username.lower())
        super().save(*args, **kwargs)
