from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/', null=True, blank=True,
        verbose_name='Аватар')

    country = models.CharField(
        max_length=256, blank=True,
        verbose_name='Страна')
    city = models.CharField(
        max_length=256, blank=True,
        verbose_name='Город')

    class Meta:
        """Перевод модели"""

        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Подписки пользователей"""
    following = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='followings',
        verbose_name='на кого подписан')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='followers',
        verbose_name='Подписчик')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Добавлен'
    )

    class Meta:
        """Перевод модели"""
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('user',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_name_owner'
            )
        ]

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписаться на самого себя.')

    def __str__(self):
        return f'Подписчик {self.user}'
