from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
EVENT_CHOICES = [
    ('add_film', 'добавил фильм в избранное'),
    ('del_film', 'удалил фильм в избранное'),
]


class EventUser(models.Model):
    """Подписки пользователей"""
    event = models.CharField(
        max_length=256, verbose_name='Событие', choices=EVENT_CHOICES)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлено'
    )

    class Meta:
        """Перевод модели"""
        verbose_name = 'событие'
        verbose_name_plural = 'События'
        ordering = ('created_at',)

    def __str__(self):
        return f'Событие {self.user}'
