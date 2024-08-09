from films.models import FilmsdModel
from django.forms import ModelForm


class AddFilmBaza(ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'
        exclude = (
            'verified', 'is_published', 'id_kp', 'poster', 'rating',
            'votecount', 'scrinshot'
        )
