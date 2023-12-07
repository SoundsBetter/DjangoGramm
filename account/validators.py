from django.core.validators import RegexValidator

from account.settings import PHONE_FMT

PHONE_REGEX = RegexValidator(
    regex=r"^\+\d{9,15}$",
    message=PHONE_FMT,
)
