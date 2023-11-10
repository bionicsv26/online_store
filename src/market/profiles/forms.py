from typing import Any
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


class UserLoginForm(AuthenticationForm):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'name': 'name', 'id': 'name', 'class': 'user-input', 'placeholder': 'E-mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'name': 'pass', 'id': 'name', 'placeholder': "********"}))

    def __init__(self, request, *args, **kwargs):
        super(UserLoginForm, self).__init__(request, *args, **kwargs)

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется.')
        return data
    

class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'name': 'name', 'id': 'name', 'class': 'user-input', 'placeholder': 'Имя'}))
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'name': 'login', 'id': 'name', 'class': 'user-input', 'placeholder': 'E-mail'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'name': 'pass', 'id': 'name', 'placeholder': 'Пароль'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется.')
        return data


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError('Email уже используется.')
        return data
    