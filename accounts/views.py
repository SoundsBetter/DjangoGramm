from django.contrib import messages
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
)

from django.http import HttpRequest, HttpResponseBase, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from accounts.forms import UserProfileForm
from accounts.models import Follower
from DjangoGramm.text_messages import (
    NOT_HAVE_ACCESS,
    PROFILE_UPD_SUCCESS,
    USER_DELETE_SUCCESS_MSG,
)
from auths.forms import UserForm
from auths.models import User


class UserAccountView(View):
    template_name = "accounts/profile.html"

    def dispatch(
        self, request: HttpRequest, *args, **kwargs
    ) -> HttpResponseBase:
        user_id = kwargs.get("user_id")
        if request.user.pk != user_id:
            messages.error(request, NOT_HAVE_ACCESS)
            return redirect(request.META.get("HTTP_REFERER", "home"))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request: HttpRequest, user_id: int) -> HttpResponseBase:
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

    def post(self, request: HttpRequest, user_id: int) -> HttpResponseBase:
        if request.POST.get("action") == "delete":  # type:ignore
            return self.delete(request, user_id)

        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.userprofile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, PROFILE_UPD_SUCCESS)
            return redirect("accounts:profile", user_id=user_id)

        return render(
            request,
            self.template_name,
            {
                "user_form": user_form,
                "profile_form": profile_form,
                "user_id": user_id,
            },
        )

    def delete(self, request: HttpRequest, user_id: int) -> HttpResponseBase:
        user = get_object_or_404(User, pk=user_id)
        if hasattr(user, "userprofile"):
            user.userprofile.delete()
        user.delete()
        messages.success(request, USER_DELETE_SUCCESS_MSG)
        return redirect("home")


class UsersListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all().order_by("username")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_name"] = "All users"
        return context


class FollowingList(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(followers__follower=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_name"] = "Following"
        return context


class FollowersList(LoginRequiredMixin, ListView):
    model = User
    template_name = "accounts/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(following__followed=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_name"] = "Followers"
        return context


class FollowUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response_data = {"followed": True, "followers_count": 0}
        user_to_follow = get_object_or_404(User, pk=pk)
        if user_to_follow != request.user:
            try:
                follower = Follower.objects.get(
                    follower=request.user, followed=user_to_follow
                )
                follower.delete()
                response_data["followed"] = False
            except Follower.DoesNotExist:
                Follower.objects.create(
                    follower=request.user, followed=user_to_follow
                )
                response_data["followed"] = True
            response_data["followers_count"] = user_to_follow.followers.count()
            return JsonResponse(response_data)


class CheckFollowView(LoginRequiredMixin, View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        response_data = {"followed": False}
        try:
            Follower.objects.get(follower=request.user, followed=user)
            response_data["followed"] = True
        except Follower.DoesNotExist:
            pass
        return JsonResponse(response_data)
