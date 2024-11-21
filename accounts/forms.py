from django import forms
from cloudinary.forms import CloudinaryFileField

from accounts.models import UserProfile
from accounts.validators import PHONE_REGEX


class UserProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        validators=[PHONE_REGEX],
        required=False,
        max_length=17,
        widget=forms.TextInput(attrs={"type": "tel"}),
    )

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )
    avatar = CloudinaryFileField(required=False)

    class Meta:
        model = UserProfile
        fields = ("avatar", "phone_number", "date_of_birth", "bio")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].options = {"tags": "avatar", "format": "png"}
