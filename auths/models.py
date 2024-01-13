from django.contrib.auth.models import AbstractUser
from django.apps import apps
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, default=None, unique=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        UserProfile = apps.get_model("accounts", "UserProfile")

        if not hasattr(self, "userprofile"):
            UserProfile.objects.create(user=self)
