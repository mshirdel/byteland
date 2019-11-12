from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Story, StoryComment


class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['story_url', 'title', 'story_body_text']
        widgets = {
            'story_url': forms.URLInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'story_body_text': forms.Textarea(attrs={'class': 'form-control'})
        }


class StoryCommentForm(forms.ModelForm):
    class Meta:
        model = StoryComment
        fields = ['story_comment']
        widgets = {
            'story_comment': forms.Textarea(attrs={'class': 'form-control'})
        }


class SearchForm(forms.Form):
    q = forms.CharField()
