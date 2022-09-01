from django import forms

from .models import Post, Images


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'description', 'place', 'category', 'status', 'image', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'place': forms.TextInput(attrs={'class': 'forms-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control-file', 'multiple': False})
        }


class ImagesForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ['images']
        widgets = {
            'images': forms.ClearableFileInput(attrs={'multiple': True}),  # to add multiple images
        }
