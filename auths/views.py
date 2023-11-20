from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from account.models import UserProfile
from auths.forms import EmailOnlyRegistrationForm, LoginForm
from auths.utils import send_confirmation_email


def register(request):
    if request.method == "POST":
        form = EmailOnlyRegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = User.objects.make_random_password()
            username = email
            user = User(email=email)
            user.username = username
            user.set_password(password)
            user.is_active = False
            user.save()
            send_confirmation_email(request, user, password)
            return redirect("home")
    else:
        form = EmailOnlyRegistrationForm()
    return render(request, "auths/registration.html", {"form": form})


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user_profile = UserProfile(user_id=user.id)
        user.save()
        user_profile.save()
        return HttpResponse("<h1>Activation success</h1>")
    else:
        return HttpResponse("<h1>Activation failure</h1>")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("account:profile", user.id)
    else:
        form = LoginForm()
    return render(request, "auths/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("home")
