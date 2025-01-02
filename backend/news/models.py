from django.db import models
from django.contrib.auth import get_user_model
from films.models import FilmsdModel


User = get_user_model()
EVENT_CHOICES = [
    ('add_film', 'добавил фильм в избранное'),
    ('del_film', 'удалил фильм из избранного'),
    ('follow_user', 'подписался на пользователя'),
    ('unfollow_user', 'отписался от пользователя'),
    ('add_comment', 'оставил отзыв на фильм'),
    ('del_comment', 'удалил свой отзыв на фильм'),
    ('edit_profile', 'изменил информацию в своей учетной записи')
]


class EventUser(models.Model):
    """Подписки пользователей"""
    event = models.CharField(
        max_length=256, verbose_name='Событие', choices=EVENT_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    film = models.ForeignKey(
        FilmsdModel, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='Фильм', related_name='film_events'
    )
    related_user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True,
        verbose_name='Связанный пользователь',
        related_name='related_user_events'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        """Перевод модели"""
        verbose_name = 'событие'
        verbose_name_plural = 'События'
        ordering = ('-created_at',)

    def __str__(self):
        return f'Событие {self.user}'
