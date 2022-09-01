from django import forms
from .models import Gallery, Photo


class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ["title", "description", "status"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["title", "short_description", "image", "status", "source", "how_often", "send_reminder"]
