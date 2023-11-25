from django.urls import path

from posts import views

app_name = "posts"
urlpatterns = [
    path("<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("feed/", views.get_all_posts, name="feed"),
    path("<int:user_id>/create/", views.create_post, name="create_post"),
    path("like/<int:post_id>/", views.like_post, name="like_post"),
    path("add_hashtags/<int:post_id>/", views.add_hashtags, name="add_hashtags"),
]
