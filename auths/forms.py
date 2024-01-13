from django.contrib.auth.forms import AuthenticationForm
from django import forms

from auths.models import User


class EmailOnlyRegistrationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="login")
    password = forms.CharField(label="password", widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
