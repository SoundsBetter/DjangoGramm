from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path(
        "<int:pk>/edit/",
        views.UpdatePost.as_view(),
        name="edit_post",
    ),
    path(
        "<int:pk>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
    path(
        "<int:pk>/delete/",
        views.DeletePost.as_view(),
        name="delete_post",
    ),
    path(
        "photos/<int:pk>/delete/",
        views.DeletePhoto.as_view(),
        name="delete_photo",
    ),
    path(
        "",
        views.PostsListView.as_view(),
        name="post_list",
    ),
    path(
        "following/",
        views.PostsFollowingListView.as_view(),
        name="post_following_list",
    ),
    path(
        "accounts/<int:user_id>/create/",
        views.CreatePostView.as_view(),
        name="create_post",
    ),
    path(
        "like/<int:pk>/",
        views.LikePostView.as_view(),
        name="like_post",
    ),
    path(
        "check_like/<int:pk>/",
        views.CheckLikeView.as_view(),
        name="check_like",
    ),
    path(
        "add_comment/<int:post_id>/",
        views.AddCommentView.as_view(),
        name="add_comment",
    ),
]
