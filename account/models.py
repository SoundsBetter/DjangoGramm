from functools import partial

from django.contrib.auth.models import User
from django.db import models

from DjangoGramm.settings import AVATARS
from DjangoGramm.utils import directory_path


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=partial(directory_path, base_folder=AVATARS),
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Date of birth"
    )
    phone_number = models.CharField(
        max_length=17,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.username
