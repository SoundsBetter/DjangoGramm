from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseBase, HttpRequest
from django.shortcuts import render, redirect

from account.forms import UserProfileForm
from account.models import UserProfile
from DjangoGramm.text_messages import NOT_HAVE_ACCESS, PROFILE_UPD_SUCCESS
from auths.forms import UserForm


@login_required
def profile(request: HttpRequest, user_id: int) -> HttpResponseBase:
    if request.user.id != user_id:
        messages.error(request, NOT_HAVE_ACCESS)
        return redirect(request.META.get("HTTP_REFERER", "home"))

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, PROFILE_UPD_SUCCESS)
            return redirect("account:profile", user_id=user_id)
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(
        request,
        "account/profile.html",
        {
            "user_form": user_form,
            "profile_form": profile_form,
            "user_id": user_id,
        },
    )


@login_required
def get_all_users(request: HttpRequest) -> HttpResponseBase:
    users = User.objects.all()
    return render(
        request,
        "account/all_users.html",
        {"users": users, "user_id": request.user.id},
    )


@login_required
def delete_user(request: HttpRequest, user_id: int) -> HttpResponseBase:
    User.objects.get(pk=user_id).delete()
    return redirect("home")


@receiver(post_delete, sender=UserProfile)
def delete_user_media_files(sender, instance, **kwargs):
    instance.avatar.delete(save=False)
