from django.urls import path

from . import views

app_name = "auths"
urlpatterns = [
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
]
