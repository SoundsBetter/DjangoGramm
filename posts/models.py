from functools import partial

from django.db import models
from django.db.models import UniqueConstraint

from DjangoGramm.settings import PICTURES
from DjangoGramm.utils import directory_path
from auths.models import User


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    caption = models.CharField(max_length=250)
    content = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    hashtags = models.ManyToManyField("Hashtag", blank=True)


class Photo(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="photos"
    )
    picture = models.ImageField(
        upload_to=partial(directory_path, base_folder=PICTURES)
    )


class Hashtag(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Like(models.Model):
    post = models.ForeignKey(
        "Post", related_name="likes", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["post", "user"], name="user_like_post")
        ]
