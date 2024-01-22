from django import forms

from posts.models import Post, Photo, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Post
        fields = ("caption", "content")


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ("picture",)


class PhotoFormEdit(forms.ModelForm):
    picture = forms.ImageField(required=False)

    class Meta:
        model = Photo
        fields = ("picture",)


class HashtagForm(forms.Form):
    hashtags = forms.CharField(max_length=50, required=False)


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="comment")

    class Meta:
        model = Comment
        fields = ("content",)
