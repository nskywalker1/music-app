from django import forms
from .models import Track

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        fields = ['title', 'audio_file', 'cover', 'album']
