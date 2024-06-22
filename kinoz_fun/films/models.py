from django.db import models
from django.contrib.auth import get_user_model
# from django.utils import timezone


User = get_user_model()


class FilmsdModel(models.Model):
    """Базовая модель"""

    is_published = models.BooleanField(
        default=True, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )
    name = models.CharField(max_length=256, verbose_name='Название')
    name_orig = models.CharField(
        max_length=256, verbose_name='Оригинальное', blank=True
    )
    year = models.IntegerField(verbose_name='Год')
    poster = models.TextField(verbose_name='Постер')
    country = models.TextField(default='Не известно', verbose_name='Страна')
    genres = models.TextField(default='Не известно', verbose_name='Жанр')
    rating = models.FloatField(verbose_name='Рейтинг', blank=True)
    votecount = models.IntegerField(verbose_name='Голосов', blank=True)
    description = models.TextField(
        default='Нет описания', verbose_name='Описание'
    )
    cat = models.CharField(max_length=256, verbose_name='Категория')
    scrinshot = models.TextField(verbose_name='Скриншоты', blank=True)

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ('created_at',)

    # def __str__(self) -> str:
    #     return self.name
