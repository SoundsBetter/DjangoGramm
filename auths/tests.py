from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, Client
from django.urls import reverse

from django.contrib.messages import get_messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from DjangoGramm.text_messages import (
    REG_SUCCESS_MSG,
    ACTIVATE_SUCCESS_MSG,
    ACTIVATE_ERROR_MSG,
)
from auths.models import User


class AuthsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user", password="secret", email="test@example.com"
        )

    def test_login_view_valid(self):
        response = self.client.post(
            reverse("auths:login"),
            {"username": "test_user", "password": "secret"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(
            getattr(response, "url", None),
            reverse("accounts:profile", kwargs={"user_id": self.user.pk}),
        )

    def test_register_view_valid(self):
        response = self.client.post(
            reverse("auths:register"), {"email": "test_valid@example.com"}
        )

        user = User.objects.get(email="test_valid@example.com")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_valid@example.com")
        self.assertFalse(user.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(getattr(response, "url", None), reverse("home"))

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            REG_SUCCESS_MSG,
            str(messages[0]),
        )

    def test_register_view_invalid_email(self):
        response = self.client.post(
            reverse("auths:register"), {"email": "invalid_email"}
        )
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Enter a valid email address.")

    def test_register_view_duplicate_email(self):
        response = self.client.post(
            reverse("auths:register"), {"email": "test@example.com"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User with this Email already exists.")

    def test_activate_view_success(self):
        user = User.objects.create_user(
            username="test_user2",
            email="test2@example.com",
            password="testpassword",
        )
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

        activation_url = reverse(
            "auths:activate", kwargs={"uidb64": uidb64, "token": token}
        )

        response = self.client.get(activation_url)

        user.refresh_from_db()
        self.assertTrue(user.is_active)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            getattr(response, "url", None),
            reverse("accounts:profile", kwargs={"user_id": user.pk}),
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), ACTIVATE_SUCCESS_MSG)

    def test_activate_view_failure_wrong_token(self):
        user = User.objects.create(pk=123, is_active=False, email="123")
        test_cases = [{"uid": 123}, {"uid": 789}]
        for test_case in test_cases:
            activation_url = reverse(
                "auths:activate",
                kwargs={
                    "uidb64": urlsafe_base64_encode(
                        force_bytes(test_case["uid"])
                    ),
                    "token": "invalidtoken",
                },
            )

            response = self.client.get(activation_url)

            self.assertFalse(user.is_active)

            self.assertEqual(response.status_code, 302)
            self.assertEqual(getattr(response, "url", None), reverse("home"))

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(
                str(messages[0]),
                ACTIVATE_ERROR_MSG,
            )
