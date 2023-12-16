from django.forms import ModelForm
from .models import Product, ProductFeedback

class ProductFeedbackForm(ModelForm):
    class Meta:
        model = ProductFeedback
        fields = ['feedback_text']
        labels = {
            "feedback_text": "Ваш отзыв",
        }
        help_texts = {
            "feedback_text": "Напишите свой бомбический отзыв прямо здесь",
        }
