from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from films.models import Favorite
from users.models import Follow
from .models import EventUser


@receiver(post_save, sender=Favorite)
def favorite_add_film(sender, instance, created, **kwargs):
    if created:
        EventUser.objects.create(
            user=instance.user,
            event='add_film',
            film=instance.film
        )


@receiver(post_delete, sender=Favorite)
def favorite_delete_film(sender, instance, **kwargs):
    EventUser.objects.create(
        user=instance.user,
        event='del_film',
        film=instance.film
    )


@receiver(post_save, sender=Follow)
def follow_add_user(sender, instance, created, **kwargs):
    if created:
        EventUser.objects.create(
            user=instance.user,
            event='follow_user',
            related_user=instance.following
        )


@receiver(post_delete, sender=Follow)
def follow_delete_user (sender, instance, **kwargs):
    EventUser.objects.create(
        user=instance.user,
        event='unfollow_user',
        related_user=instance.following
    )
