import os
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from films.models import Favorite, Coment, Torrent
from news.models import EventUser
from .middleware import is_from_admin
from .models import Follow


@receiver(post_delete, sender=Torrent)
def delete_torrent_file(sender, instance, **kwargs):
    """Удаление файла после удаление записи"""
    if instance.file and os.path.isfile(instance.file.path):
        os.remove(instance.file.path)


@receiver(post_save, sender=Favorite)
def favorite_add_film(sender, instance, created, **kwargs):
    """Добавил фильм в избраное"""
    if created and not is_from_admin():
        EventUser.objects.create(
            user=instance.user,
            event='add_film',
            film=instance.film
        )


@receiver(post_delete, sender=Favorite)
def favorite_delete_film(sender, instance, **kwargs):
    """Удалил фильм из избраного"""
    if not is_from_admin():
        EventUser.objects.create(
            user=instance.user,
            event='del_film',
            film=instance.film
        )


@receiver(post_save, sender=Follow)
def follow_add_user(sender, instance, created, **kwargs):
    """Подписался на пользователя"""
    if created and not is_from_admin():
        EventUser.objects.create(
            user=instance.user,
            event='follow_user',
            related_user=instance.following
        )


@receiver(post_delete, sender=Follow)
def follow_delete_user(sender, instance, **kwargs):
    """Отписался от пользователя"""
    if not is_from_admin():
        EventUser.objects.create(
            user=instance.user,
            event='unfollow_user',
            related_user=instance.following
        )


@receiver(post_save, sender=Coment)
def add_comment(sender, instance, created, **kwargs):
    """Добавил комментарий"""
    if created and not is_from_admin():
        EventUser.objects.create(
            user=instance.author,
            event='add_comment',
            film=instance.film
        )


@receiver(post_delete, sender=Coment)
def delet_comment(sender, instance, **kwargs):
    """Удалил комментарий"""
    if not is_from_admin():
        EventUser.objects.create(
            user=instance.author,
            event='del_comment',
            film=instance.film
        )
