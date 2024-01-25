from cloudinary.models import CloudinaryField
from django.db import models
from django.db.models import UniqueConstraint


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
    picture = CloudinaryField("picture")

    def delete(self, *args, **kwargs):
        file = self.picture
        super().delete(*args, **kwargs)
        file.delete(save=False)


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


class Comment(models.Model):
    post = models.ForeignKey(
        "Post", related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    content = models.TextField(max_length=280, blank=False)
