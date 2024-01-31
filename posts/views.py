from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import OuterRef, Exists, Prefetch
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)

from auths.models import User
from posts.forms import (
    PostForm,
    PhotoForm,
    PhotoFormEdit,
    HashtagForm,
    CommentForm,
)
from posts.models import Post, Photo, Like, Comment
from DjangoGramm.text_messages import (
    POST_CREATED_SUCCESS_MSG,
    POST_CREATED_DENIED_MSG,
    POST_EDIT_SUCCESS_MSG,
    CREATE_POST_SUBMIT,
    UPDATE_POST_SUBMIT,
    BAD_REQUEST,
)
from posts.utils import hashtag_handler
from posts.mixins import UserIsOwnerMixin


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/create_post.html"

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'

    def dispatch(self, request: HttpRequest, *args, **kwargs):
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


class UpdatePost(UserIsOwnerMixin, LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/edit_post.html"

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'

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
            user = get_object_or_404(User, pk=user_id)
            context["profile_user"] = user
        context["feed_name"] = "All posts"
        context["comment_form"] = CommentForm()
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
            queryset.select_related("user", "user__userprofile")
            .prefetch_related("photos", "hashtags", "likes")
            .order_by("-created_at")
        )
        likes = Like.objects.filter(user=self.request.user, post=OuterRef("pk"))
        comment_prefetch = Prefetch(
            "comments",
            queryset=Comment.objects.select_related("user__userprofile"),
        )
        queryset = queryset.prefetch_related(comment_prefetch).annotate(
            user_like_it=Exists(likes)
        )
        hashtag, user_id = self._get_query_params()
        if hashtag:
            queryset = queryset.filter(hashtags__name=hashtag)
        elif user_id:
            try:
                user_id = int(user_id)
            except ValueError as ex:
                messages.error(BAD_REQUEST, ex)
                return redirect("home")
            queryset = queryset.filter(user__id=user_id)
        return queryset


class PostsFollowingListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/feed.html"
    context_object_name = "posts"

    def _get_followed_users(self):
        return User.objects.filter(followers__follower=self.request.user)

    def get_queryset(self):
        followed_users = self._get_followed_users()
        queryset = super().get_queryset()
        queryset = (
            queryset.filter(user__in=followed_users)
            .select_related("user__userprofile")
            .prefetch_related("photos", "hashtags", "likes")
            .prefetch_related(
                Prefetch(
                    "comments",
                    queryset=Comment.objects.select_related(
                        "user__userprofile"
                    ),
                )
            )
            .annotate(
                user_like_it=Exists(
                    Like.objects.filter(
                        user=self.request.user, post=OuterRef("pk")
                    )
                )
            )
            .order_by("-created_at")
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feed_name"] = "Following"
        return context


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = get_object_or_404(Post, pk=post_id)
            comment.save()
            return JsonResponse(
                {
                    "status": "success",
                    "message": "Comment added",
                    "username": request.user.username,
                    "comment": comment.content,
                }
            )
        else:
            return JsonResponse({"status": "error", "message": "Invalid form"})


class DeletePost(UserIsOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Post

    def get_success_url(self):
        return f'{reverse_lazy("posts:post_list")}?user={self.request.user.pk}'


class DeletePhoto(UserIsOwnerMixin, LoginRequiredMixin, DeleteView):
    model = Photo

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER", "home")


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        response_data = {"liked": False, "likes_count": 0}
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(post=post, user=request.user)
            like.delete()
            response_data["liked"] = False
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=request.user)
            response_data["liked"] = True
        response_data["likes_count"] = post.likes.count()
        return JsonResponse(response_data)


class CheckLikeView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        response_data = {"liked": False}
        try:
            Like.objects.get(post=post, user=request.user)
            response_data["liked"] = True

        except Like.DoesNotExist:
            pass
        return JsonResponse(response_data)
