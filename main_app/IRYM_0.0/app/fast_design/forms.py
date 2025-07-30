from django import forms
from .models import FastDesign

class FastDesignForm(forms.ModelForm):
    class Meta:
        model = FastDesign
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'put a Title'
            }),
        }
        labels = {
            'title': 'Title',
        }
        
class EditForm(forms.Form):
    prompt = forms.CharField(max_length=500)