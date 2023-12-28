from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseBase
from django.urls import reverse
from django.views.generic import DetailView, ListView

from auths.models import User
from posts.forms import PostForm, PhotoForm, PhotoFormEdit, HashtagForm
from posts.models import Post, Photo, Like
from DjangoGramm.text_messages import (
    POST_CREATED_SUCCESS_MSG,
    POST_CREATED_DENIED_MSG,
    POST_EDIT_DENIED_MSG,
    POST_EDIT_SUCCESS_MSG,
    UNLIKE_DENIED_MSG,
    LIKE_IT_MSG,
    CREATE_POST_SUBMIT,
    UPDATE_POST_SUBMIT,
    BAD_REQUEST,
    NOT_HAVE_ACCESS,
)
from posts.utils import hashtag_handler


@login_required
def create_post(request: HttpRequest, user_id: int) -> HttpResponseBase:
    if user_id != request.user.id:
        messages.error(request, POST_CREATED_DENIED_MSG)
        return redirect(request.META.get("HTTP_REFERER", "home"))

    if request.method == "POST":
        post_form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        hashtag_form = HashtagForm(request.POST)
        if (
            post_form.is_valid()
            and photo_form.is_valid()
            and hashtag_form.is_valid()
        ):
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            photo = photo_form.save(commit=False)
            photo.post = post
            photo.save()
            hashtags = hashtag_form.cleaned_data.get("hashtags")
            if hashtags:
                hashtag_handler(post=post, hashtags=hashtags.split())
            messages.success(request, POST_CREATED_SUCCESS_MSG)
            return redirect(f"{reverse('posts:post_list')}?user={user_id}")
    else:
        post_form = PostForm()
        photo_form = PhotoForm()
        hashtag_form = HashtagForm()
    return render(
        request,
        "posts/create_post.html",
        {
            "post_form": post_form,
            "photo_form": photo_form,
            "hashtag_form": hashtag_form,
            "user_id": user_id,
            "submit_button": CREATE_POST_SUBMIT,
        },
    )


@login_required
def edit_post(request: HttpRequest, post_id: int) -> HttpResponseBase:
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        messages.error(request, POST_EDIT_DENIED_MSG)
        return redirect(request.META.get("HTTP_REFERER", "home"))

    if request.method == "POST":
        post_form = PostForm(request.POST)
        photo_form = PhotoFormEdit(request.POST, request.FILES)
        hashtag_form = HashtagForm(request.POST)
        if post_form.is_valid() and hashtag_form.is_valid():
            post.caption = post_form.cleaned_data["caption"]
            post.content = post_form.cleaned_data["content"]
            post.save()
            if "picture" in request.FILES:
                photo = photo_form.save(commit=False)
                photo.post = post
                photo.save()
            hashtags = hashtag_form.cleaned_data.get("hashtags")
            if hashtags:
                hashtag_handler(
                    post=post, hashtags=hashtags.split()  # type: ignore
                )
            messages.success(request, POST_EDIT_SUCCESS_MSG)
            return redirect(
                f"{reverse('posts:post_list')}?user={request.user.id}"
            )
    else:
        post_form = PostForm(instance=post)
        photo_form = PhotoFormEdit()
        hashtag_form = HashtagForm()
    return render(
        request,
        "posts/edit_post.html",
        {
            "post_form": post_form,
            "photo_form": photo_form,
            "hashtag_form": hashtag_form,
            "user_id": request.user.id,
            "post": post,
            "submit_button": UPDATE_POST_SUBMIT,
        },
    )


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related("user__userprofile").prefetch_related(
            "photos", "hashtags", "likes"
        )


class PostsListView(LoginRequiredMixin, ListView):
    model = Post
    context_object_name = "posts"

    def _get_query_params(self):
        hashtag = self.request.GET.get("hashtag")  # type: ignore
        user_id = self.request.GET.get("user")  # type: ignore
        return hashtag, user_id

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.GET.get("user")  # type: ignore

        if user_id:
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                user = None
            context["profile_user"] = user

        return context

    def get_template_names(self):
        hashtag, user_id = self._get_query_params()
        if user_id:
            return ["posts/user_posts.html"]
        else:
            return ["posts/feed.html"]

    def get_queryset(self):
        queryset = super().get_queryset()
        hashtag, user_id = self._get_query_params()
        if hashtag:
            queryset = (
                queryset.filter(hashtags__name=hashtag)
                .select_related("user__userprofile")
                .prefetch_related("photos", "hashtags")
                .annotate(likes_count=Count("likes"))
                .order_by("-created_at")
            )
        elif user_id:
            try:
                user_id = int(user_id)
            except ValueError as ex:
                messages.error(BAD_REQUEST, ex)
                return redirect("home")
            queryset = (
                queryset.filter(user__id=user_id)
                .select_related("user__userprofile")
                .prefetch_related("photos", "hashtags")
                .annotate(likes_count=Count("likes"))
                .order_by("-created_at")
            )

        return (
            queryset.select_related("user__userprofile")
            .prefetch_related("photos", "hashtags")
            .annotate(likes_count=Count("likes"))
            .order_by("-created_at")
        )


@login_required
def delete_post(request: HttpRequest, post_id: int) -> HttpResponseBase:
    if post_id != request.user.id:
        messages.error(request, NOT_HAVE_ACCESS)
        return redirect(request.META.get("HTTP_REFERER", "home"))

    Post.objects.get(pk=post_id).delete()
    return redirect(f"{reverse('posts:post_list')}?user={request.user.id}")


@login_required
def delete_photo(request: HttpRequest, photo_id: int) -> HttpResponseBase:
    Photo.objects.get(pk=photo_id).delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def like_post(request: HttpRequest, post_id: int) -> HttpResponseBase:
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(user_id=request.user.id).exists():
        Like.objects.filter(post_id=post_id, user_id=request.user.id).delete()
        messages.error(request, UNLIKE_DENIED_MSG)
    else:
        Like.objects.create(post_id=post_id, user_id=request.user.id)
        messages.success(request, LIKE_IT_MSG)
    return redirect(request.META.get("HTTP_REFERER", "home"))


@receiver(post_delete, sender=Photo)
def delete_post_media_files(sender, instance, **kwargs):
    instance.picture.delete(save=False)
