from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Follow


User = get_user_model()


class EmailUpdateForm(forms.ModelForm):
    """Форма для изменения email"""
    class Meta:
        model = User
        fields = ['email']


class AvatarForm(forms.ModelForm):
    """Форма для изменения email"""
    class Meta:
        model = User
        fields = ['avatar']


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
