from django import forms

from posts.models import Post, Photo


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Post
        fields = ("caption", "content")


class PhotoFormEdit(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Photo
        fields = ("picture",)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("picture",)


class HashtagForm(forms.Form):
    hashtags = forms.CharField(max_length=50)
