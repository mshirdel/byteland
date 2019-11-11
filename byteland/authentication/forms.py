from django import forms
from django.utils.translation import gettext as _

from .models import User


class RegisterUserForm(forms.ModelForm):
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('Reapet password'),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            if email and User.objects.get(email=email):
                raise forms.ValidationError('Email address must be unique')
        except User.DoesNotExist:
            return email


class ResendEmailActivationForm(forms.Form):
    email = forms.EmailField(label=_('Email'),
                                     widget=forms.EmailInput(
                                         attrs={'class': 'form-control'}))
