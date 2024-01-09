from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("<int:user_id>/", views.UserAccountView.as_view(), name="profile"),
    path("", views.AllUsersView.as_view(), name="get_all_users"),
    path("<int:pk>/follow/", views.FollowUserView.as_view(), name="follow"),
    path(
        "<int:pk>/check_follow/",
        views.CheckFollowView.as_view(),
        name="check_follow",
    ),
]
