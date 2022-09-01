from django import forms
from django.contrib.auth.models import User

from .models import UserProfile, NewsletterUser


class UserProfileForm(forms.ModelForm):
    # user = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    # profile_image = forms.ImageField(widget=forms.widgets.FileInput())

    class Meta:
        model = UserProfile
        fields = ['name', 'bio', 'location', 'birth_date', 'profile_image']


class ContactForm(forms.Form):
    email = forms.EmailField(max_length=150, label='Email Address')
    name = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=100, label='Subject')
    message = forms.CharField(max_length=1500, widget=forms.Textarea, label="Message Content", required=True)
    send_to_me = forms.BooleanField(required=False, label='Send to me')


class NewsletterUserSignUpForm(forms.ModelForm):
    class Meta:
        model = NewsletterUser
        fields = ['email']

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email


class UserDeleteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = []   # delete form has only submitted button, empty "fields" list still necessary

