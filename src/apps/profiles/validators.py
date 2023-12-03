from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.safestring import SafeString

from urllib.parse import urlsplit

from .enums import SocialNetWorkEnum


class SocialNetworkValidator(URLValidator):
    DOMAINS: set = SocialNetWorkEnum.get_values()

    def __call__(self, value) -> None:
        super().__call__(value)
        parse = urlsplit(value)
        self.message = self._generate_message()
        # if domain is invalid or path is empty
        if (parse.netloc not in self.DOMAINS) or (
            parse.path.replace("/", "").strip() == ""
        ):
            raise ValidationError(self.message, code=self.code, params={"value": value})

    def _generate_message(self) -> SafeString:
        array_of_networks: list = [net.name for net in SocialNetWorkEnum]
        networks: str = ", ".join(array_of_networks)
        message: str = f"<p style='background-color: red;'>ENTER URL OF FOLLOWING NETWORKS: {networks}\n</p>"
        return format_html(message)
