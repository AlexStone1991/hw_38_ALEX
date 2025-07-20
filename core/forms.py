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
        queryset=Service.objects.all(),  
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = Order
        fields = ["master", 'client_name', 'phone', 'appointment_date', 'services', 'comment']
        widgets = {
            "client_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
            "phone": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 999-99-99'
            }),

            "comment": forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий к заказу'
            }),
            'services': forms.CheckboxSelectMultiple(
                attrs={'class': 'form-control'}
            ),

            'appointment_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            
            "master": forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_master' 
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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