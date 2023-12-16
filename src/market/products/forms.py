from django.forms import ModelForm
from django.forms import Textarea
from .models import Product, ProductFeedback


class ProductFeedbackForm(ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['feedback_text']
        widgets = {
            'feedback_text': Textarea(attrs={
                "class": "form-textarea",
                "name": "review",
                "id": "review",
                "placeholder": "Отзыв"
            })
        }
