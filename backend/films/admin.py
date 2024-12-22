from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings
from . models import FilmsdModel, Category, Genres, Country, Coment
from django.contrib.admin.models import LogEntry


class FilmsdModelForm(forms.ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmsdModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id_kp:
            if 'id_kp' in self.fields:
                text_h = (
                    'Ссылка кинопоиска: '
                    f'<a href="https://www.kinopoisk.ru/film/{self.instance.id_kp}"'
                    'target="_blank">'
                    f'https://www.kinopoisk.ru/film/{self.instance.id_kp}</a>'
                    '<br>Ссылка на фильм: '
                    f'<a href="/film/{self.instance.id_kp}/"'
                    f'target="_blank">{self.instance.id_kp}</a>'
                )
                self.fields['id_kp'].help_text = format_html(text_h)
            if 'poster' in self.fields:
                image = self.instance.poster.split(',')
                self.fields['poster'].help_text = format_html(
                    f'<a href="{image[0]}" target="_blank">'
                    f'<img src="{image[1]}" alt="Image" '
                    f'style="max-height: 100px; max-width: 100px;">'
                )


class FilmsCountMixin(admin.ModelAdmin):
    list_display = (
        'name',
        'films_count',
        'created_at',
    )
    search_fields = ['name',]
    list_per_page = settings.OBJECTS_PER_PAGE

    @admin.display(description='Количество фильмов')
    def films_count(self, obj):
        return obj.posts.count()


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Записи в журнале"""
    list_display = (
        'action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_flag', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message')
    list_per_page = settings.OBJECTS_PER_PAGE


@admin.register(FilmsdModel)
class FilmsAdmin(admin.ModelAdmin):
    form = FilmsdModelForm
    list_display = (
        'image_preview',
        'id_kp',
        'name',
        'created_at',
        'is_published',
        'verified'
    )
    list_display_links = ('name',)
    search_fields = ['name', 'id_kp']
    list_filter = ('is_published', 'verified')
    list_per_page = settings.OBJECTS_PER_PAGE

    @admin.display(description='Постер')
    def image_preview(self, obj):
        """Показывать миниатюру изображения"""
        image = obj.poster.split(',')
        if obj.poster:
            return mark_safe(
                f'<img src="{image[1]}" alt="Image" '
                f'style="max-height: 100px; max-width: 100px;"/>'
            )
        return 'Нет изображения'


@admin.register(Coment)
class ComentAdmin(admin.ModelAdmin):
    list_display = (
        'image_preview',
        'text',
        'author',
        'film_name',
        'created_at',
    )
    list_display_links = ('text',)
    list_per_page = settings.OBJECTS_PER_PAGE
    list_filter = ('author',)

    @admin.display(description='Название фильма')
    def film_name(self, obj):
        url = reverse('admin:films_filmsdmodel_change', args=[obj.film.id])
        return format_html(f'<a href="{url}">{obj.film.name}</a>')

    @admin.display(description='Постер')
    def image_preview(self, obj):
        """Показывать миниатюру изображения"""
        image = obj.film.poster.split(',')
        if obj.film.poster:
            return mark_safe(
                f'<img src="{image[1]}" alt="Image" '
                f'style="max-height: 100px; max-width: 100px;"/>'
            )
        return 'Нет изображения'


@admin.register(Category)
class CategoryAdmin(FilmsCountMixin):
    list_display_links = ('name',)
    search_fields = ['name']


@admin.register(Genres)
class GenresAdmin(FilmsCountMixin):
    pass


@admin.register(Country)
class CountryAdmin(FilmsCountMixin):
    pass
