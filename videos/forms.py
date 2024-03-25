from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from video_project import settings
from .models import Video
from django import forms

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'publisher', 'producer', 'genre', 'age_rating', 'video_file')

    def __init__(self, *args, **kwargs):
        super(VideoUploadForm, self).__init__(*args, **kwargs)
        # Applying Bootstrap 'form-control' class to each form field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

from django import forms
from .models import CommentRating
class CommentRatingForm(forms.ModelForm):
    class Meta:
        model = CommentRating
        fields = ['text', 'rating']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment...', 'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'placeholder': 'Rating (1-5)', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        rating = cleaned_data.get('rating')

        if not text and not rating:
            raise forms.ValidationError('You must either leave a comment or give a rating.')

        return cleaned_data