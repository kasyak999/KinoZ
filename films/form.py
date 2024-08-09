from films.models import FilmsdModel
from django.forms import ModelForm
from django.core.exceptions import ValidationError


BAD_WORDS = (
    '666',
    # Дополните список на своё усмотрение.
)
WARNING = 'Не ругайтесь!'


class AddFilmBaza(ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'
        exclude = (
            'verified', 'is_published', 'poster', 'rating',
            'votecount', 'scrinshot'
        )

    # def clean_text(self):
    #     id_kp = self.cleaned_data['id_kp']
    #     if id_kp == '666':
    #         raise ValidationError(WARNING)
    #     return id_kp
