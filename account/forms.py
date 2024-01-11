from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

User = get_user_model()


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(label='Your email address', required=True, validators=[EmailValidator, ])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''

    def clean_email(self):
        email = self.cleaned_data['email'].lower()

        # email unique validator
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email is already in use')

        return email
