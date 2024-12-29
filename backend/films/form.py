from django import forms
from films.models import FilmsdModel, Coment, Favorite


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
