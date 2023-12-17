from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.views import View

from accounts.models import UserProfile
from auths.forms import EmailOnlyRegistrationForm, LoginForm
from DjangoGramm.text_messages import (
    USER_EXISTS_MSG,
    REG_SUCCESS_MSG,
    ACTIVATE_SUCCESS_MSG,
    ACTIVATE_ERROR_MSG,
)
from auths.utils import send_confirmation_email


def register(request: HttpRequest) -> HttpResponseBase:
    if request.method == "POST":
        form = EmailOnlyRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = User.objects.make_random_password()
            username = email

            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                user = User(email=email)
                user.username = username
                user.set_password(password)
                user.is_active = False
                user.save()
                send_confirmation_email(user=user, password=password)
                messages.success(request, REG_SUCCESS_MSG)
                return redirect("home")
            messages.error(request, USER_EXISTS_MSG % email)
            return redirect("home")
    else:
        form = EmailOnlyRegistrationForm()
    return render(request, "auths/register.html", {"form": form})


def activate(request: HttpRequest, uidb64: str, token: str) -> HttpResponseBase:
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user_profile = UserProfile(user_id=user.id)
            user.save()
            user_profile.save()

            login(request, user)

            messages.success(request, ACTIVATE_SUCCESS_MSG)
            return redirect("accounts:profile", user_id=user.id)
        else:
            messages.error(request, ACTIVATE_ERROR_MSG)
            return redirect("home")

    except User.DoesNotExist:
        messages.error(request, ACTIVATE_ERROR_MSG)
        return redirect("home")


def login_view(request: HttpRequest) -> HttpResponseBase:
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("accounts:profile", user.id)
    else:
        form = LoginForm()
    return render(request, "auths/login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")
