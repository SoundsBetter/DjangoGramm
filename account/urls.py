from django.urls import path

from account import views

app_name = "account"
urlpatterns = [
    path("<int:user_id>/profile/", views.profile, name="profile"),
]
