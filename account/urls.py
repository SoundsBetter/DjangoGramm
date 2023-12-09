from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("<int:user_id>/profile/", views.profile, name="profile"),
    path("<int:user_id>/delete/", views.delete_user, name="delete_user"),
    path("", views.get_all_users, name="get_all_users"),
]
