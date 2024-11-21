from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render, redirect


def home(request: HttpRequest) -> HttpResponseBase:
    if request.user.is_authenticated:
        return redirect("posts:post_list")
    return render(request, "home.html")


def handler404(request, exception):
    return render(request, "404.html", {})
