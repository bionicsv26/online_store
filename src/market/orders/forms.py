import re

from django import forms


class OrderCreationForm(forms.Form):
    def clean(self):
        for field_name, field in self.fields.items():
            if field_name in self.errors.as_data():
                field.widget.attrs.update({'class': 'form-input form-input_error'})

        return super().clean()


class OrderCreationPage1Form(OrderCreationForm):
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
        return data

    def clean_phone(self):
        data = self.cleaned_data['phone']
        if re.fullmatch(r'\+7 \(\d{3}\) \d{7}', data) is None:
            self.add_error('phone', 'Номер должен состоять из кода региона и 10 цифр')
        return data


class OrderCreationPage2Form(OrderCreationForm):
    delivery_city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label='Город',
    )
    delivery_address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        label='Адрес',
    )
    delivery_method = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[('ordinary', 'Обычная доставка'), ('express', 'Экспресс доставка')],
        label='Способ доставки',
        initial='ordinary'
    )


class OrderCreationPage3Form(OrderCreationForm):
    payment_method = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=[('online', 'Онлайн картой'), ('someone', 'Онлайн со случайного чужого счета')],
        label='Способ оплаты',
        initial='online',
    )
