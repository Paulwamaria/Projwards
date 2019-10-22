from django import forms
from django.contrib.auth.models import User
from .models import Vote



class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote

        fields = ['design_votes', 'content_votes', 'usability_votes','creativity_votes']