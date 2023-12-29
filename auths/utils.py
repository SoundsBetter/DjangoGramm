import string
import typing as t

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.crypto import get_random_string

from DjangoGramm.settings import EMAIL_HOST_USER, ACTIVATE_URL
from DjangoGramm.text_messages import EMAIL_MSG, EMAIL_SUBJECT
from auths.models import User

USERTYPE = t.TypeVar("USERTYPE", bound=User)
PASSWORD_LENGTH = 15
ALLOWED_CHARS = string.ascii_letters + string.digits + "!@#$%^&*()-_+="


def send_confirmation_email(user: USERTYPE, password: str) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"{ACTIVATE_URL}/{uid}/{token}/"
    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_MSG % {"link": link, "password": password},
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    print(password, link)


def make_random_password(
    length: int = PASSWORD_LENGTH, allowed_chars: str = ALLOWED_CHARS
):
    return get_random_string(length, allowed_chars)
