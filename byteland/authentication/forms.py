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
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email address must be unique')
        return email


class ResendEmailActivationForm(forms.Form):
    email = forms.EmailField(label=_('Email'),
                             widget=forms.EmailInput(
        attrs={'class': 'form-control'}))


class EditUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True,
                               label='Username',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))

    class Meta():
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        email_exist = User.objects.filter(email=email).exclude(username=username)
        if email and email_exist:
            raise forms.ValidationError('Email address must be unique')
        else:
            return email
