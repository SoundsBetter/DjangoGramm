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
        "photos/<int:photo_id>/delete/",
        views.delete_photo,
        name="delete_photo",
    ),
    path(
        "",
        views.PostsListView.as_view(),
        name="post_list",
    ),
    path(
        "accounts/<int:user_id>/create/",
        views.CreatePostView.as_view(),
        name="create_post",
    ),
    path(
        "like/<int:post_id>/",
        views.like_post,
        name="like_post",
    ),
    path(
        "temp/",
        views.temp,
        name="temp",
    ),
]
