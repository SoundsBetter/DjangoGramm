from django import forms

from posts.models import Post, Photo


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("caption",)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("picture",)
