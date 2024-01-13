from django.urls import path, re_path

from . import views

app_name = "auths"
urlpatterns = [
    path("login/", views.AuthsLoginView.as_view(), name="login"),
    path("logout/", views.AuthsLogoutView.as_view(), name="logout"),
    path("signup/", views.AuthsSignupView.as_view(), name="signup"),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.AuthsConfirmEmailView.as_view(),
        name="account_confirm_email",
    ),
    path(
        "confirm-email/",
        views.EmailVerificationSentView.as_view(),
        name="account_email_verification_sent",
    ),
]
