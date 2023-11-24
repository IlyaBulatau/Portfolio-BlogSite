from enum import Enum


class SocialNetWorkEnum(Enum):
    GITHUB = "github.com"
    TELEGRAM = "t.me"
    LINKEDIN = "linkedin.com"

    @classmethod
    def get_values(cls) -> set:
        values = [cls._member_map_.get(values).value for values in cls._member_names_]
        return set(values)
