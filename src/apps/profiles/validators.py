from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlsplit

from abc import ABC
import re


class BaseURLValidator(ABC, URLValidator):

    def __init__(self, netloc=None, schemes=None, **kwargs):
        super().__init__(schemes=None, **kwargs)
        self.netloc = (
            netloc if netloc
            else self.netloc 
            if self.netloc
            else None
            )

    def __call__(self, value) -> None:
        super().__call__(value)
        if self.netloc:
            parse = urlsplit(value)
            if parse.netloc != self.netloc:
                raise ValidationError(self.message, code=self.code, params={"value": value})


class GitHubURLValidator(BaseURLValidator):
    netloc = "github.com"
        

class TelegramURLValidator(BaseURLValidator):
    netloc = "t.me"


class LinkedInURLValidator(BaseURLValidator):
    netloc = "linkedin.com"
