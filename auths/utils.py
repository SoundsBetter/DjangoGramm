from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from DjangoGramm.settings import EMAIL_HOST_USER


def send_confirmation_email(request, user, password):
    current_site = get_current_site(request)
    domain = current_site.domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link = f"http://{domain}/auths/activate/{uid}/{token}/"
    message = f"Thank you for registering! Please click the link below to confirm your email:\n\n{link}\n\n Your {password=}"
    print(message)
    subject = "Activate your account"
    from_email = EMAIL_HOST_USER  # Replace with your email address
    to_email = user.email
    send_mail(subject, message, from_email, [to_email])
