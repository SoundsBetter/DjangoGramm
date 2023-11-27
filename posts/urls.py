from django.urls import path

from . import views

app_name = "posts"
urlpatterns = [
    path(
        "feed/",
        views.get_feed,
        name="feed",
    ),
    path(
        "<int:post_id>/edit/",
        views.edit_post,
        name="edit_post",
    ),
    path(
        "<int:post_id>/delete/",
        views.delete_post,
        name="delete_post",
    ),
    path(
        "photos/<int:photo_id>/delete/",
        views.delete_photo,
        name="delete_photo",
    ),
    path(
        "account/<int:user_id>/",
        views.get_user_posts,
        name="get_user_posts",
    ),
    path(
        "account/<int:user_id>/create/",
        views.create_post,
        name="create_post",
    ),
    path(
        "like/<int:post_id>/",
        views.like_post,
        name="like_post",
    ),
]
