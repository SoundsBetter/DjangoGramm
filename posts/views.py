from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponseBase
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

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


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'

    def dispatch(self, request, *args, **kwargs):
        if self.kwargs.get("user_id") != self.request.user.pk:
            messages.error(self.request, POST_CREATED_DENIED_MSG)
            return redirect(self.request.META.get("HTTP_REFERER", "home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()

        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.post = post
            photo.save()

        hashtag_form = HashtagForm(self.request.POST)
        if hashtag_form.is_valid():
            hashtags = hashtag_form.cleaned_data.get("hashtags")
            if hashtags:
                hashtag_handler(post=post, hashtags=hashtags.split())

        messages.success(self.request, POST_CREATED_SUCCESS_MSG)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["photo_form"] = PhotoForm(
                self.request.POST, self.request.FILES
            )
            context["hashtag_form"] = HashtagForm(self.request.POST)
        else:
            context["photo_form"] = PhotoForm()
            context["hashtag_form"] = HashtagForm()
            context["submit_button"] = CREATE_POST_SUBMIT
            context["title"] = "Create"
        return context


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/edit_post.html"

    def __init__(self):
        self.object = None

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(Post, pk=kwargs["pk"])
        if request.user != self.object.user:
            messages.error(self.request, POST_EDIT_SUCCESS_MSG)
            return redirect(self.request.META.get("HTTP_REFERER", "home"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        photo_form = PhotoForm(self.request.POST, self.request.FILES)
        if photo_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.post = self.object
            photo.save()

        hashtag_form = HashtagForm(self.request.POST)
        if hashtag_form.is_valid():
            hashtags = hashtag_form.cleaned_data.get("hashtags")
            if hashtags:
                hashtag_handler(post=self.object, hashtags=hashtags.split())
        messages.success(self.request, POST_EDIT_SUCCESS_MSG)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context["photo_form"] = PhotoFormEdit(
                self.request.POST, self.request.FILES
            )
            context["hashtag_form"] = HashtagForm(self.request.POST)
        else:
            context["photo_form"] = PhotoFormEdit()
            context["hashtag_form"] = HashtagForm()
            context["submit_button"] = UPDATE_POST_SUBMIT
            context["title"] = "Update"
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"

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
        queryset = (
            queryset.select_related("user__userprofile")
            .prefetch_related("photos", "hashtags")
            .annotate(likes_count=Count("likes"))
            .order_by("-created_at")
        )
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
        return queryset


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'


@login_required
def delete_post(request: HttpRequest, pk: int) -> HttpResponseBase:
    post = Post.objects.get(pk=pk)
    if post.user.pk != request.user.pk:
        messages.error(request, NOT_HAVE_ACCESS)
        return redirect(request.META.get("HTTP_REFERER", "home"))

    post.delete()
    return redirect(f"{reverse('posts:post_list')}?user={request.user.pk}")


@login_required
def delete_photo(request: HttpRequest, photo_id: int) -> HttpResponseBase:
    Photo.objects.get(pk=photo_id).delete()
    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def like_post(request: HttpRequest, post_id: int) -> HttpResponseBase:
    post = get_object_or_404(Post, pk=post_id)
    if post.likes.filter(user_id=request.user.pk).exists():
        Like.objects.filter(post_id=post_id, user_id=request.user.pk).delete()
        messages.error(request, UNLIKE_DENIED_MSG)
    else:
        Like.objects.create(post_id=post_id, user_id=request.user.pk)
        messages.success(request, LIKE_IT_MSG)
    return redirect(request.META.get("HTTP_REFERER", "home"))


@receiver(post_delete, sender=Photo)
def delete_post_media_files(sender, instance, **kwargs):
    instance.picture.delete(save=False)


def temp(request):
    post = Post.objects.get(pk=2)
    return render(request, "posts/temp.html", {"post": post})
