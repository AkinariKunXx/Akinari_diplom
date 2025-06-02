from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'phone', 'payment_method']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('card', 'Карта'),
                ('cash', 'Наличные'),
            ])
        }