from django.urls import path

from . import views
from .views import ProfileView, AllUsersView

app_name = "account"
urlpatterns = [
    path("<int:user_id>/profile/", ProfileView.as_view(), name="profile"),
    path("<int:user_id>/delete/", views.delete_user, name="delete_user"),
    path("", AllUsersView.as_view(), name="get_all_users"),
]
