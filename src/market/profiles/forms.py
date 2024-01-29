import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.models import User
from .models import Profile
from django.utils.translation import gettext_lazy as _


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email уже используется.')
        return data


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': _(
            "Please enter a correct email and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email is not None and password:
            self.user_cache = authenticate(self.request, email=email, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'email': 'email'},
        )

class UserSetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    new_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password')
        password_validation.validate_password(password1, self.user)
        return password1

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

class UserProfileForm(forms.Form):
    avatar = forms.ImageField(label='Аватар')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password_repeat = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')

    full_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'name'}),
        label='ФИО',
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+7 (___) _______', 'id': 'phone'}),
        label='Телефон',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input', 'id': 'mail'}),
        label='E-mail',
    )

    def clean_full_name(self):
        data = self.cleaned_data['full_name']
        split_data = data.split()
        if not ''.join(split_data).isalpha():
            self.add_error('full_name', 'Это поле может содержать только буквы и пробелы')
        if len(split_data) != 3:
            self.add_error('full_name', 'Это поле должно состоять из 3-х слов')
        for i_name in split_data:
            if not i_name[0].isupper():
                self.add_error('full_name', 'Фамилия, Имя и Отчество должно быть с заглавной буквы')
                break
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if re.fullmatch(r'\+7 \(\d{3}\) \d{7}', data) is None:
            self.add_error('phone', 'Номер должен состоять из кода региона и 10 цифр')
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if re.fullmatch(regex, data) is None:
            self.add_error('email', 'Не правильный формат электронной почты')
        return data
