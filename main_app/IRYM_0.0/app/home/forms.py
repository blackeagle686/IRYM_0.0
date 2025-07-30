from django import forms

class EditWithAIForm(forms.Form):
    image = forms.ImageField(required=True, label="Upload Image")
    prompt = forms.CharField(
        required=True,
        label="Edit Prompt",
    )

