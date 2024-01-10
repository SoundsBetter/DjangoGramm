from django import forms

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
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = UserProfile
        fields = ("avatar", "phone_number", "date_of_birth")
