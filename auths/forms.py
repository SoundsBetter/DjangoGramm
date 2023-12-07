from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms


class EmailOnlyRegistrationForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["email"]


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="login")
    password = forms.CharField(label="password", widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")
