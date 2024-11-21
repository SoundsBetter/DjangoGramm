from allauth.account.views import (
    LoginView,
    SignupView,
    LogoutView,
    ConfirmEmailView,
)
from django.views.generic import TemplateView


class AuthsSignupView(SignupView):
    template_name = "auths/signup.html"


class AuthsLoginView(LoginView):
    template_name = "auths/login.html"


class AuthsLogoutView(LogoutView):
    template_name = "auths/logout.html"


class AuthsConfirmEmailView(ConfirmEmailView):
    template_name = "auths/email_confirm.html"


class EmailVerificationSentView(TemplateView):
    template_name = "auths/verification_sent.html"
