# forms.py
from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    # You can customize the form fields or add extra validation if needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply Bootstrap styling to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'



from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',  # Add Bootstrap class for styling
                'placeholder': 'Enter title here'  # Optional: add a placeholder
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',  # Add Bootstrap class for styling
                'rows': 5,
                'placeholder': 'Enter content here'  # Optional: add a placeholder
            }),
        }
