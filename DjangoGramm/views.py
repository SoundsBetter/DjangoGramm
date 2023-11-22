from django.http import HttpResponse
from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated:
        return redirect("account:profile", user_id=request.user.id)
    return render(request, "home.html")
