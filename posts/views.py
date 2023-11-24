from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostForm, PhotoForm
from posts.models import Post, Like


@login_required
def create_post(request, user_id):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if post_form.is_valid() and photo_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            photo = photo_form.save(commit=False)
            photo.post = post
            photo.save()
            messages.success(request, "Post was created successfully")
            return redirect("account:profile", user_id=user_id)
    else:
        post_form = PostForm()
        photo_form = PhotoForm()

    return render(
        request,
        "posts/create_post.html",
        {"post_form": post_form, "photo_form": photo_form, "user_id": user_id},
    )


@login_required
def get_all_post_of_user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(
        request, "posts/posts_of_user.html", {"user": user, "user_id": user_id}
    )


@login_required
def get_all_posts(request):
    posts = Post.objects.order_by("-created_at")
    return render(
        request, "posts/feed.html", {"posts": posts, "user_id": request.user.id}
    )


@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        post_form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if post_form.is_valid() and photo_form.is_valid():
            post = Post.objects.get(pk=post_id)
            post.caption = post_form.cleaned_data["caption"]
            post.save()
            photo = photo_form.save(commit=False)
            photo.post = post
            photo.save()
            messages.success(request, "Пост було успішно відредаговано")
            return redirect("account:profile", user_id=request.user.id)
    else:
        post_form = PostForm(instance=Post.objects.get(pk=post_id))
        photo_form = PhotoForm()
    return render(
        request,
        "posts/edit_post.html",
        {"post_form": post_form, "photo_form": photo_form, "user_id": request.user.id},
    )


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        messages.error(request, "Can't like post 2 times.")
        return redirect("posts:feed")

    like = Like(post=post, user=request.user)
    like.save()
    messages.success(request, "You liked it.")
    return redirect("posts:feed")
