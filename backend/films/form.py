from films.models import FilmsdModel, Coment
# from django.forms import ModelForm, HiddenInput
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()
BAD_WORDS = (
    '666',
    # Дополните список на своё усмотрение.
)
WARNING = 'Не ругайтесь!'


class EmailUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']


class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ('text',)


class AddFilmBaza(forms.ModelForm):

    class Meta:
        model = FilmsdModel
        fields = '__all__'
        exclude = (
            'verified', 'is_published'
        )
        # fields = [
        #     'id_kp',
        #     'name',
        #     'name_orig',
        #     'year',
        #     'description',
        #     'poster',
        #     'scrinshot',
        #     'genres',
        #     'country'
        # ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем скрытое поле
        for value in ['poster', 'scrinshot', 'rating', 'votecount']:
            self.fields[value].widget = forms.HiddenInput()
        # Устанавливаем поле id_kp как доступное только для чтения
        for value in ['id_kp', 'name', 'name_orig', 'year', 'description']:
            self.fields[value].widget.attrs['readonly'] = True
        # # Убираем подсказку для поля poster
        # self.fields['name'].help_text += '111111'


class CustomUserCreationForm(UserCreationForm):
    """Форма для регистрации"""
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
