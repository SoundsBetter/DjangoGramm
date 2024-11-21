from django import forms
from cloudinary.forms import CloudinaryFileField

from posts.models import Post, Photo, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Post
        fields = ("caption", "content")


class PhotoForm(forms.ModelForm):
    picture = CloudinaryFileField()

    class Meta:
        model = Photo
        fields = ["picture"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].options = {"tags": "photo", "format": "png"}


class PhotoFormEdit(forms.ModelForm):
    picture = CloudinaryFileField(required=False)

    class Meta:
        model = Photo
        fields = ("picture",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].options = {"tags": "photo", "format": "png"}


class HashtagForm(forms.Form):
    hashtags = forms.CharField(max_length=50, required=False)


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="comment")

    class Meta:
        model = Comment
        fields = ("content",)
