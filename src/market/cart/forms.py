from django import forms

class CartOrderCreateForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,)