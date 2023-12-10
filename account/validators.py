from django.core.validators import RegexValidator

from DjangoGramm.text_messages import PHONE_FMT

PHONE_REGEX = RegexValidator(
    regex=r"^\+\d{9,15}$",
    message=PHONE_FMT,
)
