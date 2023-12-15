from django.forms import ModelForm
from .models import Product, ProductFeedback

class ProductFeedbackForm(ModelForm):
    class Meta:
        model = ProductFeedback
        fields = 'feedback_text',
