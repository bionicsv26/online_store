from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'search-input',
        'placeholder': 'Введите запрос',
    }))
