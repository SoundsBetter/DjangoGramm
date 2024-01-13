from allauth.account.views import (
    LoginView,
    SignupView,
    LogoutView,
    ConfirmEmailView,
)
from allauth.socialaccount.providers.oauth2.views import OAuth2CallbackView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponseBase, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.views import View
from django.views.generic import TemplateView

from accounts.models import UserProfile
from auths.forms import EmailOnlyRegistrationForm, LoginForm
from DjangoGramm.text_messages import (
    USER_EXISTS_MSG,
    REG_SUCCESS_MSG,
    ACTIVATE_SUCCESS_MSG,
    ACTIVATE_ERROR_MSG,
    LOGIN_FAIL_MSG,
)
from auths.models import User
from auths.utils import send_confirmation_email, make_random_password


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
