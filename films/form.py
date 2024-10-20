from films.models import FilmsdModel, Coment
from django.forms import ModelForm, HiddenInput
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()
BAD_WORDS = (
    '666',
    # Дополните список на своё усмотрение.
)
WARNING = 'Не ругайтесь!'


class ComentForm(ModelForm):
    class Meta:
        model = Coment
        fields = ('text',)


class AddFilmBaza(ModelForm):
    class Meta:
        model = FilmsdModel
        # fields = '__all__'
        # exclude = (
        #     'verified', 'is_published', 'rating',
        #     'votecount'
        # )
        fields = [
            'id_kp',
            'name',
            'name_orig',
            'year',
            'description',
            'poster',
            'scrinshot',
            'genres',
            'country'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем скрытое поле
        self.fields['poster'].widget = HiddenInput()
        self.fields['scrinshot'].widget = HiddenInput()
        # Устанавливаем поле id_kp как доступное только для чтения
        self.fields['id_kp'].widget.attrs['readonly'] = True
        self.fields['name'].widget.attrs['readonly'] = True
        self.fields['name_orig'].widget.attrs['readonly'] = True
        self.fields['year'].widget.attrs['readonly'] = True
        self.fields['description'].widget.attrs['readonly'] = True

        # # Устанавливаем виджет для поля poster
        # self.fields['poster'].widget = ImageWidget()
        # # Убираем подсказку для поля poster
        # self.fields['name'].help_text += '111111'
