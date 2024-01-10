from typing import Any

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super(UserCreationForm, self).__init__(*args, **kwargs)

            self.fields['email'].label = 'Your email address'
            self.fields['email'].required = True
            self.fields['username'].help_text = ''
            self.fields['password1'].help_text = ''

        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            if User.objects.filter(email=email).exists() and len(email) > 254:
                raise forms.ValidationError('Email is already in use or too long')

            return email
