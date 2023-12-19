from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Prefetch, Count
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseBase, HttpResponse
from django.views import View

from posts.forms import PostForm, PhotoForm, PhotoFormEdit, HashtagForm
from posts.models import Post, Photo, Like
from DjangoGramm.text_messages import (
    POST_CREATED_MSG,
    POST_EDIT_DENIED_MSG,
    POST_EDIT_SUCCESS_MSG,
    UNLIKE_DENIED_MSG,
    LIKE_IT_MSG,
    CREATE_POST_SUBMIT,
    UPDATE_POST_SUBMIT,
    POST_DELETE_SUCCESS_MSG,
)
from posts.utils import hashtag_handler


@login_required
def create_post(request: HttpRequest, user_id: int) -> HttpResponseBase:
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
            messages.success(request, POST_CREATED_MSG)
            return redirect("posts:get_user_posts", user_id=user_id)
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


class PostView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, post_id: int) -> HttpResponseBase:
        post = (
            Post.objects.select_related("user__userprofile")
            .prefetch_related("photos", "hashtags", "likes")
            .get(pk=post_id)
        )
        return render(request, "posts/post.html", {"post": post})

    def post(self, request: HttpRequest, post_id: int) -> HttpResponseBase:
        if request.POST.get("action") == "delete":
            return self.delete(request, post_id)

    def delete(self, request: HttpRequest, post_id: int) -> HttpResponseBase:
        post = get_object_or_404(Post, pk=post_id)
        print(post)
        post.delete()
        messages.success(request, POST_DELETE_SUCCESS_MSG)
        return redirect("posts:get_user_posts", user_id=request.user.id)


@login_required
def edit_post(request: HttpRequest, post_id: int) -> HttpResponseBase:
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        messages.error(request, POST_EDIT_DENIED_MSG)
        return redirect(request.META["HTTP_REFERER"])

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
                hashtag_handler(post=post, hashtags=hashtags.split())  # type: ignore
            messages.success(request, POST_EDIT_SUCCESS_MSG)
            return redirect("posts:get_user_posts", user_id=request.user.id)
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


@login_required
def get_user_posts(request: HttpRequest, user_id: int) -> HttpResponseBase:
    user = (
        User.objects.select_related("userprofile")
        .prefetch_related(
            Prefetch(
                "posts",
                queryset=Post.objects.prefetch_related(
                    "photos", "hashtags"
                ).annotate(likes_count=Count("likes")),
            )
        )
        .get(pk=user_id)
    )
    return render(
        request,
        "posts/user_posts.html",
        {"user": user},
    )


@login_required
def get_feed(request: HttpRequest) -> HttpResponseBase:
    posts = (
        Post.objects.all()
        .select_related("user__userprofile")
        .prefetch_related("photos", "hashtags")
        .annotate(likes_count=Count("likes"))
        .order_by("-created_at")
    )
    return render(
        request,
        "posts/feed.html",
        {"posts": posts},
    )


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


@login_required
def delete_photo(request: HttpRequest, photo_id: int) -> HttpResponseBase:
    Photo.objects.get(pk=photo_id).delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def get_posts_by_hashtag(
    request: HttpRequest, hashtag_id: int
) -> HttpResponseBase:
    posts = (
        Post.objects.select_related("user__userprofile")
        .filter(hashtags__id=hashtag_id)
        .prefetch_related("photos", "hashtags", "likes")
        .order_by("-created_at")
    )
    return render(
        request,
        "posts/feed.html",
        {"posts": posts, "user_id": request.user.id},
    )


def temp(request):
    post = get_object_or_404(Post, pk=1)
    result = Post.objects.filter(id=post.id, likes__user=request.user.id)
    return HttpResponse(f"TEMP{result}")


@receiver(post_delete, sender=Photo)
def delete_post_media_files(sender, instance, **kwargs):
    instance.picture.delete(save=False)
