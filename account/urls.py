from django.urls import path

from account import views as account
from posts import views as posts

app_name = "account"
urlpatterns = [
    path("<int:user_id>/profile/", account.profile, name="profile"),
    path(
        "<int:user_id>/posts", posts.get_all_post_of_user, name="get_all_post_of_user"
    ),
]
