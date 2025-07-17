from django import forms
from .models import Order, Service
from django.forms import DateTimeInput

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'appointment_date', 'comment']
        widgets = {
            'appointment_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, service=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.service = service
        self.fields['appointment_date'].required = True