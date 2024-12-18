from functools import partial
from django.db import models
from cloudinary.models import CloudinaryField

from DjangoGramm.settings import AVATARS
from DjangoGramm.utils import directory_path
from auths.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = CloudinaryField("avatar", null=True)
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Date of birth"
    )
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        null=True,
    )
    updated_at = models.DateTimeField(auto_now=True)

    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        file = self.avatar
        super().delete(*args, **kwargs)
        file.delete(save=False)


class Follower(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    constraints = [
        models.UniqueConstraint(
            fields=["follower", "following"], name="user_follow"
        )
    ]
