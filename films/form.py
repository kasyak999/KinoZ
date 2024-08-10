from films.models import FilmsdModel, Coment
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django import forms


BAD_WORDS = (
    '666',
    # Дополните список на своё усмотрение.
)
WARNING = 'Не ругайтесь!'


class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ('text',)


class AddFilmBaza(ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'
        exclude = (
            'verified', 'is_published', 'poster', 'rating', 'id_kp',
            'votecount', 'scrinshot'
        )

    # def clean_name(self):  # Изменяем метод на clean_name
    #     name = self.cleaned_data['name']
    #     if FilmsdModel.objects.filter(name=name).count() > 0:
    #         raise forms.ValidationError("<b>www</b>")
    #     return name

    # def clean_id_kp(self):
    #     """Проверяем, существует ли уже фильм с таким id_kp"""
    #     id_kp = self.cleaned_data['id_kp']
    #     if FilmsdModel.objects.filter(id_kp=id_kp).exists():
    #         raise forms.ValidationError(
    #             "Фильм с таким ID кинопоиска уже существует в базе."
    #             "Пожалуйста, введите другой ID."
    #         )
    #     return id_kp
