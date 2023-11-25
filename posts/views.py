from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from posts.forms import PostForm, PhotoForm
from posts.models import Post, Like, Hashtag, Photo


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
    post = Post.objects.get(pk=post_id)
    if post.user != request.user:
        messages.error(request, "You can only edit your own posts")
        return redirect(request.META["HTTP_REFERER"])

    if request.method == "POST":
        post_form = PostForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if post_form.is_valid():
            post.caption = post_form.cleaned_data["caption"]
            post.save()
            if photo_form.is_valid() and "picture" in request.FILES:
                photo = photo_form.save(commit=False)
                photo.post = post
                photo.save()

            hashtags = request.POST.getlist("hashtags")
            for hashtag_text in hashtags:
                hashtag, created = Hashtag.objects.get_or_create(name=hashtag_text)
                post.hashtags.add(hashtag)
            messages.success(request, "Post updated successfully")
            return redirect("account:get_all_post_of_user", user_id=request.user.id)
    else:
        post_form = PostForm(instance=post)
        photo_form = PhotoForm()
    return render(
        request,
        "posts/edit_post.html",
        {
            "post_form": post_form,
            "photo_form": photo_form,
            "user_id": request.user.id,
            "post": post,
        },
    )


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        messages.error(request, "Can't like post 2 times.")
        return redirect(request.META["HTTP_REFERER"])

    like = Like(post=post, user=request.user)
    like.save()
    messages.success(request, "You liked it.")
    return redirect(request.META["HTTP_REFERER"])


@login_required
def add_hashtags(request, post_id):
    if request.method == "POST":
        hashtags = request.POST.get("hashtags")
        post = get_object_or_404(Post, pk=post_id)
        for hashtag_name in hashtags.split():
            hashtag, created = Hashtag.objects.get_or_create(name=hashtag_name)
            post.hashtags.add(hashtag)
        return redirect("account:get_all_post_of_user", request.user.id)


@login_required
def delete_post(request, post_id):
    Post.objects.get(pk=post_id).delete()
    return redirect("account:get_all_post_of_user", user_id=request.user.id)


@login_required
def delete_photo(request, photo_id):
    Photo.objects.get(pk=photo_id).delete()
    return redirect(request.META["HTTP_REFERER"])
