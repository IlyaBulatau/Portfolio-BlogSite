from django.utils.translation import gettext_lazy as _


TAGS = (
    "Fastion",
    "Equipments",
    "Programming",
    "Cars",
    "Family",
    "Health",
)

TAGS_CHOISE = tuple((tag, _(tag)) for tag in TAGS)