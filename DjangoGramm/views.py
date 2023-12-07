from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render, redirect


def home(request: HttpRequest) -> HttpResponseBase:
    if request.user.is_authenticated:
        return redirect("account:get_all_users")
    return render(request, "home.html")


def handler404(request, exception):
    return render(request, "404.html", {})
