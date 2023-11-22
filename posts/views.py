from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from posts.forms import PostForm
from posts.models import Post


@login_required
def create_post(request, user_id):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, "Post was created successfully")
            return redirect("account:profile", user_id=user_id)
    else:
        form = PostForm()

    return render(request, "posts/create_post.html", {"form": form, "user_id": user_id})


@login_required
def get_all_post_of_user(request, user_id):
    user = User.objects.get(pk=user_id)
    return render(request, "posts/posts_of_user.html", {"user": user})


@login_required
def get_all_posts(request):
    posts = Post.objects.all()
    return render(request, "posts/feed.html", {"posts": posts})
