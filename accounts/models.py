from functools import partial


from django.db import models

from DjangoGramm.settings import AVATARS
from DjangoGramm.utils import directory_path
from auths.models import User


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
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        file = self.avatar
        super().delete(*args, **kwargs)
        file.delete(save=False)
