from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import render, redirect

from account.forms import UserProfileForm
from auths.forms import UserForm


@login_required
def profile(request, user_id):
    if request.user.id != user_id:
        return HttpResponseForbidden("Ви не маєте доступу до цієї сторінки.")

    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=request.user.userprofile)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile was updated successfully.")
            return redirect("account:profile", user_id=user_id)

    return render(
        request,
        "account/profile.html",
        {"user_form": user_form, "profile_form": profile_form, "user_id": user_id},
    )
