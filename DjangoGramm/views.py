from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect("account:get_all_users")
    return render(request, "home.html")
