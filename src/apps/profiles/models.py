from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from phonenumber_field.modelfields import PhoneNumberField
from urllib.parse import urlsplit

from .validators import SocialNetworkValidator
from .enums import SocialNetWorkEnum
from apps.users.models import User



class SocialNetwork(models.Model):
    NAME = {
        SocialNetWorkEnum.GITHUB.value: "GitHub",
        SocialNetWorkEnum.TELEGRAM.value: "Telegram",
        SocialNetWorkEnum.LINKEDIN.value: "LinkedIn"
    }

    name = models.CharField()
    link = models.URLField(blank=True, null=False, unique=True, validators=[SocialNetworkValidator()])
    logo = models.ImageField()
    is_active = models.BooleanField(default=True, null=False, blank=False)
    contact = models.ForeignKey(User, related_name="networks", on_delete=models.PROTECT)

    class Meta:
        db_table = "social_networks"


    def save(self, *args, **kwargs):
        link = self.link
        domain = urlsplit(link)
        name = self.NAME.get(domain.netloc, None)
        if name:
            self.name = name 
            self.logo = f"images/social/{self.name.lower()}-logo.png"
            super().save(*args, **kwargs)


    def clean(self, flag=False) -> None:
        if flag:
            raise ValidationError("Link is incorrect")
