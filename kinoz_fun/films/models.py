from django.db import models
from django.contrib.auth import get_user_model
# from django.utils import timezone
# from django.contrib.postgres.fields import JSONField
# django.db.models.JSONField

User = get_user_model()


class MainModel(models.Model):
    """Базовая модель"""
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )

    class Meta:
        abstract = True
        ordering = ('created_at',)

    def __str__(self):
        if len(self.name) > 20:
            result = self.name[:20] + '...'
        else:
            result = self.name
        return result


class FilmsdModel(MainModel):
    """Фильмы модель"""
    # image = models.URLField(max_length=200)
    is_published = models.BooleanField(
        default=False, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    id_kp = models.IntegerField(verbose_name='id кинопоиска')
    name = models.CharField(max_length=256, verbose_name='Название')
    name_orig = models.CharField(
        max_length=256, verbose_name='Оригинальное', blank=True
    )
    year = models.IntegerField(verbose_name='Год')
    poster = models.JSONField(
        default=dict, verbose_name='Постер', blank=True,
        help_text=(
            'url - оригинал, "prev - превью'
            '{"url": "ссылка", "prev": "ссылка"}'
        ),
    )
    country = models.ManyToManyField(
        'Country', verbose_name='Страна', blank=True
    )
    genres = models.ManyToManyField(
        'Genres', verbose_name='Жанр', blank=True
    )
    # null=True, verbose_name='Жанр', blank=True
    rating = models.FloatField(default=0, null=True, verbose_name='Рейтинг', blank=True)
    votecount = models.IntegerField(
        default=0, null=True, verbose_name='Голосов', blank=True
    )
    description = models.TextField(
        default='Нет описания', verbose_name='Описание'
    )
    cat = models.ForeignKey(
        'Category',
        max_length=256,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True
    )
    scrinshot = models.JSONField(
        default=list, verbose_name='Скриншоты', blank=True,
        help_text=(
            'imageUrl - оригинал, "previewUrl - превью'
            '[{"imageUrl": "ссылка", "previewUrl": "ссылка"}, ]'
        )
    )
    

    class Meta(MainModel.Meta):
        verbose_name = 'фильм'
        verbose_name_plural = 'Фильмы'
        default_related_name = 'posts'

    # def __str__(self) -> str:
    #     return self.name


class Category(MainModel):
    """Катагории фильмов"""

    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta(MainModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genres(MainModel):
    """Жанры фильмов"""

    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta(MainModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Country(MainModel):
    """Страны фильмов"""

    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta(MainModel.Meta):
        verbose_name = 'страна'
        verbose_name_plural = 'Страны'
    