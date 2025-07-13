from django import forms
from .models import Order, Service, Master

class OrderForm(forms.ModelForm):
    service = forms.ModelChoiceField(
        queryset=Service.objects.all(), 
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = Order
        fields = ['client_name', 'phone', 'comment', 'service', "master", "comment"]
        widgets = {
            "appointment_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        service = kwargs.pop('service', None)
        super().__init__(*args, **kwargs)
        if service:
            self.fields['master'].queryset = Master.objects.filter(services=service)
