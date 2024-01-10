from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=True, null=True, unique=True)
