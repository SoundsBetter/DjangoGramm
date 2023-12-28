from django.test import TestCase
from django.urls import reverse

from accounts.models import UserProfile
from auths.models import User


class AccountsViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_profile_authenticated_user(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("accounts:profile", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")
        self.assertContains(response, "Update Profile")

    def test_profile_unauthenticated_user(self):
        response = self.client.get(
            reverse("accounts:profile", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_profile_another_user(self):
        another_user = User.objects.create(
            username="another_user", password="another_test_password"
        )
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("accounts:profile", kwargs={"user_id": another_user.id})
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(getattr(response, "url", None), reverse("home"))

    def test_profile_edit_valid(self):
        self.client.login(username="test_user", password="test_password")
        data = {
            "username": "new_username",
            "first_name": "New",
            "last_name": "User",
            "email": "new_user@example.com",
            "phone_number": "+9999999999",
            "date_of_birth": "2023-11-21",
        }

        response = self.client.post(
            reverse("accounts:profile", kwargs={"user_id": self.user.id}),
            data,
            format="multipart",
        )

        self.assertEqual(response.status_code, 302)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "new_username")
        self.assertEqual(self.user.first_name, "New")
        self.assertEqual(self.user.last_name, "User")
        self.assertEqual(self.user.email, "new_user@example.com")

    def test_profile_edit_invalid(self):
        self.client.login(username="test_user", password="test_password")
        data = {
            "username": "new_username",
            "first_name": "New",
            "last_name": "User",
            "email": "new_user@example.com",
            "phone_number": "invalid_phone",
            "date_of_birth": "invalid_date",
        }

        response = self.client.post(
            reverse("accounts:profile", kwargs={"user_id": self.user.id}),
            data,
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "phone_number")
        self.assertContains(response, "date_of_birth")

    def test_get_all_users(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("accounts:get_all_users"), kwargs={"user_id": self.user.id}
        )

        self.assertEqual(response.status_code, 200)
