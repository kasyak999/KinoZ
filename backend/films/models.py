from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class MainModel(models.Model):
    """Базовая модель"""
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        if len(self.name) > 50:
            result = self.name[:50] + '...'
        else:
            result = self.name
        return result


class FilmsdModel(MainModel):
    """Фильмы модель"""
    verified = models.BooleanField(
        default=False, verbose_name='Проверено',
        help_text='Снимите галочку, если все проверено.'
    )
    is_published = models.BooleanField(
        default=False, verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    id_kp = models.IntegerField(
        verbose_name='id кинопоиска', unique=True,
    )
    name_orig = models.CharField(
        max_length=256, verbose_name='Оригинальное название',
        blank=True, null=True
    )
    year = models.IntegerField(verbose_name='Год', null=True, blank=True)
    poster = models.TextField(
        verbose_name='Постер', blank=True, null=True,
        help_text=('Пример: http://оригинал, http://превью'),
    )
    rating = models.FloatField(
        default=0, null=True, verbose_name='Рейтинг', blank=True)
    votecount = models.IntegerField(
        default=0, verbose_name='Голосов', blank=True, null=True,
    )
    description = models.TextField(
        default='Нет описания', verbose_name='Описание', null=True, blank=True
    )
    scrinshot = models.JSONField(
        null=True, verbose_name='Скриншоты', blank=True,
        help_text=(
            'imageUrl - оригинал, "previewUrl - превью'
            '[{"imageUrl": "ссылка", "previewUrl": "ссылка"}, ]'
        )
    )
    actors = models.JSONField(
        verbose_name='Актеры', null=True, blank=True
    )
    trailer = models.JSONField(
        verbose_name='Трейлеры', null=True, blank=True
    )
    cat = models.ForeignKey(
        'Category',
        max_length=256,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    country = models.ManyToManyField(
        'Country', verbose_name='Страна', blank=True,
        help_text='Зажмите Ctrl и выберите'
    )
    genres = models.ManyToManyField(
        'Genres', verbose_name='Жанр', blank=True,
        help_text='Зажмите Ctrl и выберите'
    )

    class Meta(MainModel.Meta):
        verbose_name = 'фильм'
        verbose_name_plural = 'Фильмы'
        default_related_name = 'posts'
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name}'


class Category(MainModel):
    """Катагории фильмов"""

    class Meta(MainModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'
        default_related_name = 'categories'


class Genres(MainModel):
    """Жанры фильмов"""

    class Meta(MainModel.Meta):
        verbose_name = 'жанр'
        verbose_name_plural = 'Жанры'


class Country(MainModel):
    """Страны фильмов"""
    name = models.CharField(max_length=256, verbose_name='Название')

    class Meta(MainModel.Meta):
        verbose_name = 'страна'
        verbose_name_plural = 'Страны'


class Coment(models.Model):
    """Комментарии к фильму"""
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )
    film = models.ForeignKey(
        FilmsdModel, on_delete=models.CASCADE,
        verbose_name='Фильм'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta(MainModel.Meta):
        verbose_name = 'комментарии'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at',)
        default_related_name = 'coments'

    def __str__(self) -> str:
        if len(self.text) > 50:
            result = self.text[:50] + '...'
        else:
            result = self.text
        return result


class Favorite(models.Model):
    """Избранные фильмы"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    film = models.ForeignKey(
        FilmsdModel, on_delete=models.CASCADE, verbose_name='Фильм')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )

    class Meta:
        """Перевод модели"""
        verbose_name = 'избраное'
        verbose_name_plural = 'Избраное'
        default_related_name = 'favorites'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'film'], name='unique_user_film')
        ]
        indexes = [
            models.Index(fields=['user', 'film']),
        ]

    def __str__(self):
        return f'{self.user}'
