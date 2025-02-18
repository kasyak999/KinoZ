# Generated by Django 5.1.4 on 2025-01-12 17:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('films', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.CharField(choices=[('add_film', 'добавил фильм в избранное'), ('del_film', 'удалил фильм из избранного'), ('follow_user', 'подписался на пользователя'), ('unfollow_user', 'отписался от пользователя'), ('add_comment', 'оставил отзыв на фильм'), ('del_comment', 'удалил свой отзыв на фильм')], max_length=256, verbose_name='Событие')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('film', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='film_events', to='films.filmsdmodel', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'событие',
                'verbose_name_plural': 'События',
                'ordering': ('-created_at',),
            },
        ),
    ]
