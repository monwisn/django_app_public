from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core import validators


class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=5, max_length=50,
                               validators=[validators.MaxLengthValidator, validators.MinLengthValidator])
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, validators=[validators.MaxLengthValidator])
    last_name = forms.CharField(max_length=100, validators=[validators.MaxLengthValidator])
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f": A user with that username '{username}' is already exists!\n")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(": The two password fields didn't match to each other!\n")
        if password1.isnumeric():
            raise forms.ValidationError(": Your password can't be entirely numeric!\n")
        if len(password1) < 8:
            raise forms.ValidationError(": Your password must contain at least 8 characters!\n")
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(f": A user with that email '{email}' already exists!\n")
        return email


class EditRegisterForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']  # 'password'
