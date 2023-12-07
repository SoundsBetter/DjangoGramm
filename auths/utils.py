import typing as t

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from DjangoGramm.settings import EMAIL_HOST_USER
from auths.settings import EMAIL_MSG, EMAIL_SUBJECT, ACTIVATE_URL

UserType = t.TypeVar("UserType", bound=User)


def send_confirmation_email(user: UserType, password: str) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"{ACTIVATE_URL}/{uid}/{token}/"
    send_mail(
        subject=EMAIL_SUBJECT,
        message=EMAIL_MSG % {"link": link, "password": password},
        from_email=EMAIL_HOST_USER,
        recipient_list=[user.email],
    )
    # print(password, link)
