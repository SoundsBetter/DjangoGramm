from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    AccessMixin,
)
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.http import HttpResponseBase, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView, DeleteView

from account.forms import UserProfileForm
from account.models import UserProfile
from DjangoGramm.text_messages import (
    NOT_HAVE_ACCESS,
    PROFILE_UPD_SUCCESS,
    PROFILE_UPD_ERROR,
)
from auths.forms import UserForm


class ProfileView(AccessMixin, View):
    template_name = "account/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("auths:login")

        user_id = kwargs.get("user_id")
        if request.user.id != user_id:
            messages.error(request, NOT_HAVE_ACCESS)
            return redirect(request.META.get("HTTP_REFERER", "home"))

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, user_id):
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "user_id": user_id,
            },
        )

    def post(self, request, user_id):
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
            messages.error(request, PROFILE_UPD_ERROR)

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "user_id": user_id,
            },
        )


class AllUsersView(LoginRequiredMixin, ListView):
    model = User
    template_name = "account/all_users.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all().order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.request.user.id
        return context


class DeleteUserView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    success_url = reverse_lazy("home")

    def test_func(self):
        return self.request.user.id == self.kwargs["pk"]

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Користувача успішно видалено.")
        return super().delete(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Виконуємо видалення без підтвердження через шаблон
        return self.delete(request, *args, **kwargs)


@receiver(post_delete, sender=UserProfile)
def delete_user_media_files(sender, instance, **kwargs):
    instance.avatar.delete(save=False)
