from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from films.models import Favorite, Coment
from django.contrib.auth import get_user_model
from users.models import Follow
from .models import EventUser


User = get_user_model()


@receiver(post_save, sender=Favorite)
def favorite_add_film(sender, instance, created, **kwargs):
    """Добавил фильм в избраное"""
    if created:
        EventUser.objects.create(
            user=instance.user,
            event='add_film',
            film=instance.film
        )


@receiver(post_delete, sender=Favorite)
def favorite_delete_film(sender, instance, **kwargs):
    """Удалил фильм из избраного"""
    EventUser.objects.create(
        user=instance.user,
        event='del_film',
        film=instance.film
    )


@receiver(post_save, sender=Follow)
def follow_add_user(sender, instance, created, **kwargs):
    """Подписался на пользователя"""
    if created:
        EventUser.objects.create(
            user=instance.user,
            event='follow_user',
            related_user=instance.following
        )


@receiver(post_delete, sender=Follow)
def follow_delete_user(sender, instance, **kwargs):
    """Отписался от пользователя"""
    EventUser.objects.create(
        user=instance.user,
        event='unfollow_user',
        related_user=instance.following
    )


@receiver(post_save, sender=Coment)
def add_comment(sender, instance, created, **kwargs):
    """Добавил комментарий"""
    if created:
        EventUser.objects.create(
            user=instance.author,
            event='add_comment',
            film=instance.film
        )


@receiver(post_delete, sender=Coment)
def delet_comment(sender, instance, **kwargs):
    """Удалил комментарий"""
    EventUser.objects.create(
        user=instance.author,
        event='del_comment',
        film=instance.film
    )


@receiver(post_save, sender=User)
def edit_profile(sender, instance, **kwargs):
    """Удалил комментарий"""
    EventUser.objects.create(
        user=instance,
        event='edit_profile',
    )
