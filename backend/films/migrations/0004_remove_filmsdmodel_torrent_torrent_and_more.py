# Generated by Django 5.1.4 on 2025-01-19 20:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0003_filmsdmodel_torrent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmsdmodel',
            name='torrent',
        ),
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='torrent/', verbose_name='Торрент')),
                ('film', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='films.filmsdmodel', verbose_name='Фильм')),
            ],
            options={
                'verbose_name': 'торрент',
                'verbose_name_plural': 'Торренты',
                'ordering': ('-id',),
                'default_related_name': 'torrents',
            },
        ),
        migrations.AddField(
            model_name='filmsdmodel',
            name='torrent',
            field=models.ManyToManyField(blank=True, to='films.torrent', verbose_name='Торрент'),
        ),
    ]
