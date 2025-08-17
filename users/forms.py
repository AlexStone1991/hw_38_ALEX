from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

user_model = get_user_model()


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = user_model
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if user_model.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
