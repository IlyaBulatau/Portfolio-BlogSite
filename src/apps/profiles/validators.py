from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlsplit

from abc import ABC

from .enums import SocialNetWorkEnum


class SocialNetworkValidator(URLValidator):
    DOMAINS: set = SocialNetWorkEnum.get_values()


    def __call__(self, value) -> None:
        super().__call__(value)
        parse = urlsplit(value)
        # if domain is invalid or path is empty
        if (parse.netloc not in self.DOMAINS) or (parse.path.replace("/", "").strip() == ""):
            raise ValidationError(self.message, code=self.code, params={"value": value})

