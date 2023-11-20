from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from account.forms import EditProfileForm


@login_required
def profile(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("Ви не маєте доступу до цієї сторінки.")

    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Профіль було успішно оновлено.")
            return redirect("account:profile", user_id=user_id)
    else:
        form = EditProfileForm(instance=user)

    return render(request, "account/profile.html", {"form": form, "user": user})
