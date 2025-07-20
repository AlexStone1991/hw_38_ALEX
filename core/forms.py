from django import forms
from .models import Order, Service, Review, Master
from django.forms import DateTimeInput

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["master", "rating", "client_name", "text", "photo"]
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'master': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class OrderForm(forms.ModelForm):
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),  # Изменили на all() вместо none()
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Order
        fields = ["master", 'client_name', 'phone', 'appointment_date', 'services', 'comment']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            "master": forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_master'  # Добавили ID для JavaScript
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если мастер уже выбран (при редактировании), фильтруем услуги
        if self.instance and self.instance.master:
            self.fields['services'].queryset = self.instance.master.services.all()

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        
        if master and services:
            invalid_services = services.exclude(masters=master)
            if invalid_services.exists():
                raise forms.ValidationError(
                    f"Мастер {master.name} не предоставляет выбранные услуги: "
                    f"{', '.join(s.name for s in invalid_services)}"
                )
        return cleaned_data




















# class OrderForm(forms.ModelForm):
#     class Meta:
#         model = Order
#         fields = ['client_name', 'phone', 'appointment_date', 'comment']
#         widgets = {
#             'appointment_date': DateTimeInput(attrs={'type': 'datetime-local'}),
#         }

#     def __init__(self, *args, service=None, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.service = service
#         self.fields['appointment_date'].required = True