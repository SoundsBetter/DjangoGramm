from django.contrib.auth.forms import UserChangeForm, forms
from django.contrib.auth.models import User
from django.db import transaction

from account.models import UserProfile


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

    avatar = forms.ImageField(required=False)
    phone_number = forms.CharField(max_length=20, required=False)
    date_of_birth = forms.DateField(required=False)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        # Check if the user profile exists, create it if not
        if not hasattr(user, "userprofile"):
            user_profile = UserProfile(user=user)
        else:
            user_profile = user.userprofile

        user_profile.avatar = self.cleaned_data.get("avatar")
        user_profile.phone_number = self.cleaned_data.get("phone_number")
        user_profile.date_of_birth = self.cleaned_data.get("date_of_birth")

        if commit:
            user.save()
            user_profile.save()

        return user
