from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from posts.models import Post, Hashtag, Photo
from posts.settings import LIKE_IT_MSG, LIKE_DENIED_MSG


# Create your tests here.
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
