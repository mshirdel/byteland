from django import forms
from django_jalali import forms as jforms

from .models import Profile

class EditProfileForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('photo', 'date_of_birth',)
        widgets = {
            'date_of_birth': jforms.widgets.jDateInput(
                attrs={'class': 'form-control datepicker'}
            )
        }
