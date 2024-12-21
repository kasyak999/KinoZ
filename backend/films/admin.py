from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country, Coment
from django.utils.html import format_html
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse


class FilmsdModelForm(forms.ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmsdModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id_kp:
            self.fields['id_kp'].help_text = format_html(
                f'''Ссылка кинопоиска:
                <a href="https://www.kinopoisk.ru/film/{self.instance.id_kp}"
                target="_blank">https://www.kinopoisk.ru/film/{self.instance.id_kp}</a>
                <br>Ссылка на фильм:
                <a href="/film/{self.instance.id_kp}/"
                target="_blank">{self.instance.id_kp}</a>
                '''
            )


@admin.register(FilmsdModel)
class FilmsAdmin(admin.ModelAdmin):
    form = FilmsdModelForm
    list_display = (
        'image_preview',
        'id_kp',
        'name',
        'is_published',
        'verified'
    )
    list_display_links = ('name',)
    search_fields = ['name', 'id_kp']
    list_filter = ('is_published', 'verified')

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
        'film_name',
    )
    list_display_links = ('text',)

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
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'films_count'
    )
    list_display_links = ('name',)
    search_fields = ['name']

    @admin.display(description='Количество фильмов')
    def films_count(self, obj):
        return obj.posts.count()


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'films_count'
    )

    @admin.display(description='Количество фильмов')
    def films_count(self, obj):
        return obj.posts.count()


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'films_count'
    )

    @admin.display(description='Количество фильмов')
    def films_count(self, obj):
        return obj.posts.count()
