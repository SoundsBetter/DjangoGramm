from django import forms

from account.models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("avatar", "phone_number", "date_of_birth")
