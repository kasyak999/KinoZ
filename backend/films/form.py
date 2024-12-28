from django import forms
from films.models import FilmsdModel, Coment, Favorite


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


class AddFilmFavorites(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = []

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Задаём текущего пользователя
        if self.film:
            instance.film = self.film  # Задаём выбранный фильм
        if commit:
            instance.save()
        return instance

    def __init__(self, *args, user=None, film=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.film = film
