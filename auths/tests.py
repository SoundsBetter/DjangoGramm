from io import BytesIO

from PIL import Image
from django.contrib.auth.tokens import default_token_generator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from account.models import UserProfile
from auths.settings import (
    ACTIVATE_ERROR_MSG,
    ACTIVATE_SUCCESS_MSG,
    USER_EXISTS_MSG,
    REG_SUCCESS_MSG,
)
from posts.models import Post, Photo, Hashtag
from posts.settings import LIKE_IT_MSG, LIKE_DENIED_MSG


class AuthsViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user", password="secret"
        )

    def test_login_view_valid(self):
        response = self.client.post(
            reverse("auths:login"),
            {"username": "test_user", "password": "secret"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user.is_authenticated)
        self.assertEqual(
            response.url,
            reverse("account:profile", kwargs={"user_id": self.user.id}),
        )

    def test_register_view_valid(self):
        response = self.client.post(
            reverse("auths:register"), {"email": "test@example.com"}
        )

        user = User.objects.get(email="test@example.com")
        print(user)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test@example.com")
        self.assertFalse(user.is_active)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

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
        User.objects.create(email="test@example.com")
        response = self.client.post(
            reverse("auths:register"), {"email": "test@example.com"}
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            USER_EXISTS_MSG % "test@example.com",
            str(messages[0]),
        )

    def test_activate_view_success(self):
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
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
            response.url,
            reverse("account:profile", kwargs={"user_id": user.id}),
        )

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), ACTIVATE_SUCCESS_MSG)

    def test_activate_view_failure_wrong_token(self):
        user = User.objects.create(pk=123, is_active=False)
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
            self.assertEqual(response.url, reverse("home"))

            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(
                str(messages[0]),
                ACTIVATE_ERROR_MSG,
            )


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
            reverse("account:profile", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "account/profile.html")
        self.assertContains(response, "Update Profile")

    def test_profile_unauthenticated_user(self):
        response = self.client.get(
            reverse("account:profile", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f'/auths/login/?next={reverse("account:profile", kwargs={"user_id": self.user.id})}',
        )

    def test_profile_another_user(self):
        another_user = User.objects.create(
            username="another_user", password="another_test_password"
        )
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("account:profile", kwargs={"user_id": another_user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

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
            reverse("account:profile", kwargs={"user_id": self.user.id}),
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
            reverse("account:profile", kwargs={"user_id": self.user.id}),
            data,
            format="multipart",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please correct the errors below.")
        self.assertContains(response, "phone_number")
        self.assertContains(response, "date_of_birth")

    def test_get_all_users(self):
        self.client.login(username="test_user", password="test_password")
        response = self.client.get(
            reverse("account:get_all_users"), kwargs={"user_id": self.user.id}
        )

        self.assertEqual(response.status_code, 200)


class PostsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="test_user",
            password="test_password",
        )
        self.client.login(username="test_user", password="test_password")

        self.post_1 = Post.objects.create(
            user=self.user, caption="Test Caption 1"
        )
        self.post_2 = Post.objects.create(
            user=self.user, caption="Test Caption 2"
        )

        self.hashtag = Hashtag.objects.create(name="test_hashtag")
        self.post_1.hashtags.add(self.hashtag)
        self.post_2.hashtags.add(self.hashtag)

        image = Image.new("RGB", (100, 100))
        image_io = BytesIO()
        image.save(image_io, format="JPEG")
        self.picture = SimpleUploadedFile("test_image.jpg", image_io.getvalue())

    def test_create_post(self):
        response = self.client.post(
            reverse("posts:create_post", kwargs={"user_id": self.user.id}),
            data={
                "caption": "Test Create",
                "hashtags": "tag1 tag2",
                "picture": self.picture,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse("posts:get_user_posts", kwargs={"user_id": self.user.id}),
        )

        test_post = Post.objects.get(pk=3)

        self.assertEqual(test_post.caption, "Test Create")
        self.assertTrue(
            self.user.posts.filter(
                caption="Test Create", hashtags__name="tag1"
            ).exists()
        )
        self.assertTrue(
            self.user.posts.filter(
                caption="Test Create", hashtags__name="tag2"
            ).exists()
        )

    def test_get_user_posts(self):
        response = self.client.get(
            reverse("posts:get_user_posts", kwargs={"user_id": self.user.id})
        )

        self.assertEqual(response.status_code, 200)

    def test_get_feed(self):
        response = self.client.get(reverse("posts:feed"))

        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        new_caption = "Updated Caption"
        response = self.client.post(
            reverse("posts:edit_post", kwargs={"post_id": self.post_1.id}),
            {"caption": new_caption, "hashtags": "tag1"},
        )

        self.post_1.refresh_from_db()
        self.assertEqual(self.post_1.caption, new_caption)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("posts:get_user_posts", kwargs={"user_id": self.user.id}),
        )

    def test_like_post(self):
        self.assertEqual(self.post_1.likes.count(), 0)

        response = self.client.get(
            reverse("posts:like_post", kwargs={"post_id": self.post_1.id})
        )

        self.post_1.refresh_from_db()
        self.assertEqual(self.post_1.likes.count(), 1)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(
            reverse("posts:like_post", kwargs={"post_id": self.post_1.id})
        )

        self.post_1.refresh_from_db()
        self.assertEqual(self.post_1.likes.count(), 1)

        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(str(messages[0]), LIKE_IT_MSG)
        self.assertEqual(str(messages[1]), LIKE_DENIED_MSG)

    def test_delete_post(self):
        self.assertTrue(Post.objects.filter(pk=self.post_1.id).exists())

        response = self.client.post(
            reverse("posts:delete_post", kwargs={"post_id": self.post_1.id})
        )

        self.assertFalse(Post.objects.filter(pk=self.post_1.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            reverse("posts:get_user_posts", kwargs={"user_id": self.user.id}),
        )

    def test_delete_photo(self):
        photo = Photo.objects.create(
            post_id=self.post_1.id, picture=self.picture
        )
        response = self.client.post(
            reverse("posts:delete_photo", kwargs={"photo_id": photo.id})
        )

        self.assertFalse(Photo.objects.filter(pk=photo.id).exists())
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("home"))

    def test_get_posts_by_hashtag(self):
        another_hashtag = Hashtag.objects.create(name="another_hashtag")
        post_with_another_hashtag = Post.objects.create(
            user=self.user, caption="Another Caption"
        )
        post_with_another_hashtag.hashtags.add(another_hashtag)

        response = self.client.get(
            reverse(
                "posts:posts_by_hashtag", kwargs={"hashtag_id": self.hashtag.id}
            )
        )

        self.assertContains(response, "Test Caption 1")
        self.assertContains(response, "Test Caption 2")
        self.assertNotContains(response, "Another Caption")
