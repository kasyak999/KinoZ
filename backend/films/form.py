from django import forms
from films.models import FilmsdModel, Coment, Favorite
from django.core.exceptions import ValidationError


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


class ComentForm(forms.ModelForm):

    class Meta:
        model = Coment
        fields = ('text',)

    def save(self, commit=True, author=None, film=None):
        instance = super().save(commit=False)
        instance.author = author
        instance.film = film
        instance.save()
        return instance


class AddFilmFavorites(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []

    def save(self, commit=True, user=None, film=None):
        instance = super().save(commit=False)
        instance.user = user  # Задаём текущего пользователя
        instance.film = film  # Задаём выбранный фильм
        instance.save()
        return instance


class FilmLinkForm(forms.Form):
    """Форма для ввода ссылки на фильм"""
    film_id = forms.CharField(label='Ссылка на кинопоск', max_length=255)

    def clean_film_id(self):
        """Валидация и обработка ссылки на фильм"""
        film_id = self.cleaned_data['film_id']
        result = film_id.split('/')
        if 'https:' not in result:
            raise ValidationError('Ссылка на фильм не соответствует формату')

        try:
            id_film = int(result[4])
        except (ValueError, TypeError, IndexError):
            raise ValidationError('Неверный формат ссылки')

        # # Проверка наличия фильма в базе
        # if FilmsdModel.objects.filter(id_kp=id_film).exists():
        #     raise ValidationError('Фильм уже есть в базе')

        return id_film  # Возвращаем `id_film` для использования
