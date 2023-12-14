from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("<int:user_id>/profile/", views.ProfileView.as_view(), name="profile"),
    path(
        "<int:pk>/delete/",
        views.DeleteUserView.as_view(),
        name="delete_user",
    ),
    path("", views.AllUsersView.as_view(), name="get_all_users"),
]
