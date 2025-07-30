from django import forms
from .models import DesignProject

class DesignProjectForm(forms.ModelForm):
    class Meta:
        model = DesignProject
        fields = ['title', 'description', 'goal', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your design project...'
            }),
            'goal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Logo, Poster, Character...'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'title': 'Title',
            'description': 'Description',
            'goal': 'Design Goal',
            'status': 'Status',
        }


class EditImageForm(forms.Form):
    uploaded_image = forms.ImageField(label="Upload an image to edit")
    edit_prompt = forms.CharField(
        label="What would you like to change?",
        widget=forms.Textarea(attrs={
            "placeholder": "e.g. make it night, add a glowing moon, change background to a forest...",
            "rows": 3
        })
    )
