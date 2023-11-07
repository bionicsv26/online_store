from django import forms
from django.core.exceptions import ValidationError


class PayForm(forms.Form):
    card_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-input Payment-bill",
        'id': "numero1",
        'name': "numero1",
        'type': "text",
        'placeholder': "9999 9999 9999 9999",
        'data-mask': "9999 9999 9999 9999",
    }))

    def clean_card_number(self):
        data = ''.join(self.cleaned_data.get('card_number').split())
        if not data.isdigit():
            raise ValidationError('Введите число из 16 цифр')
        elif int(data) % 2 != 0:
            raise ValidationError('Номер должен быть четным')
        elif int(data) % 10 == 0:
            raise ValidationError('Номер не должен заканчиваться на 0')
        elif len(data) != 16:
            raise ValidationError('Номер должен состоять из 16 цифр')

        return data
