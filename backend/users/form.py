from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class EmailUpdateForm(forms.ModelForm):
    """Форма для изменения email"""
    class Meta:
        model = User
        fields = ['email']


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
