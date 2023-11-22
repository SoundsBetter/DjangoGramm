from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    picture = models.ImageField(upload_to=f"pictures/")
    caption = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
