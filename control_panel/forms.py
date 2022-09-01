from django import forms

from main.models import Newsletter


class NewsletterCreationForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ['subject', 'body', 'email', 'status']
