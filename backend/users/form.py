from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Follow, Message
from django.core.exceptions import ValidationError


User = get_user_model()


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'avatar', 'username', 'email', 'first_name', 'last_name',
            'country', 'city'
        ]


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AddFollow(forms.ModelForm):
    class Meta:
        model = Follow
        fields = ['user', 'following']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

    # def clean(self):
    #     """Глобальная валидация для проверки sender и receiver"""
    #     cleaned_data = super().clean()

    #     sender = cleaned_data.get('sender')
    #     receiver = cleaned_data.get('receiver')

    #     # Проверка, чтобы sender и receiver не были одинаковыми
    #     if sender and receiver and sender == receiver:
    #         raise ValidationError("Нельзя отправить сообщение самому себе.")

    #     return cleaned_data
