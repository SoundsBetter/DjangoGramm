from django.contrib.auth.models import User
from django.db import models

from account.utils import user_directory_path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Date of birth"
    )
    phone_number = models.CharField(
        max_length=17,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username
