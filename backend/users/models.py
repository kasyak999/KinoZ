from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class UserProfile(AbstractUser):
    avatar = models.ImageField(
        upload_to='users/', null=True, blank=True,
        verbose_name='Аватар')

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
        UserProfile, on_delete=models.CASCADE, related_name='following',
        verbose_name='на кого подписан')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='follower',
        verbose_name='Подписчик')

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
        default_related_name = 'follows'

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписаться на самого себя.')

    def __str__(self):
        return f'Подписчик {self.user}'
