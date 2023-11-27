import typing as t

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from DjangoGramm.settings import EMAIL_HOST_USER
from auths.settings import EMAIL_MSG, EMAIL_SUBJECT

UserType = t.Type[User]


def send_confirmation_email(
    request: HttpRequest, user: UserType, password: str
) -> None:
    current_site = get_current_site(request)
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"http://{domain}/auths/activate/{uid}/{token}/"
    message = EMAIL_MSG % {"link": link, "password": password}
    print(message)
    subject = EMAIL_SUBJECT
    from_email = EMAIL_HOST_USER
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])
