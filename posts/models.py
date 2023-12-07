from django.db import models
from django.contrib.auth.models import User

from posts.utils import user_directory_path


class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["post", "user"]


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(
        User, through="Like", related_name="liked_posts"
    )
    hashtags = models.ManyToManyField("Hashtag", blank=True)


class Photo(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="photos"
    )
    picture = models.ImageField(upload_to=user_directory_path)


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)
