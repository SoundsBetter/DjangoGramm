from django.urls import path

from posts import views

app_name = "posts"
urlpatterns = [
    path("feed/", views.get_all_posts, name="feed"),
    path("<int:user_id>/", views.get_all_post_of_user, name="get_all_post_of_user"),
    path("<int:user_id>/create/", views.create_post, name="create_post"),
]
