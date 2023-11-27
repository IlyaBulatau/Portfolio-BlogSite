from enum import Enum


class SocialNetWorkEnum(Enum):
    GITHUB = "github.com"
    TELEGRAM = "t.me"
    LINKEDIN = "linkedin.com"

    @classmethod
    def get_values(cls) -> set:
        values = [item.value for item in cls]
        return set(values)
