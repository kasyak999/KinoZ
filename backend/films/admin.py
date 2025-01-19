import json
from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.conf import settings
from django.contrib.admin.models import LogEntry
from django.contrib import messages
from django.db.models import Count, JSONField
from django_json_widget.widgets import JSONEditorWidget
from . models import (
    FilmsdModel, Category, Genres, Country, Coment, Favorite, Torrent)


@admin.action(description='Проверено')
def verified(modeladmin, request, queryset):
    queryset.update(verified=True)
    messages.success(
        request, "Выбранные записи были успешно отмечены как проверено.")


@admin.action(description='Не проверено')
def not_verified(modeladmin, request, queryset):
    queryset.update(verified=False)
    messages.success(
        request, "Выбранные записи были успешно отмечены как не проверено.")


@admin.action(description='Опубликовано')
def is_published(modeladmin, request, queryset):
    queryset.update(is_published=True)
    messages.success(
        request, "Выбранные записи были успешно отмечены как опубликовано.")


@admin.action(description='Не опубликовано')
def not_is_published(modeladmin, request, queryset):
    queryset.update(is_published=False)
    messages.success(
        request, "Выбранные записи были успешно отмечены как не опубликовано.")


class PrettyJSONEncoder(json.JSONEncoder):
    """Для красивого отображения Json"""
    def __init__(self, *args, indent, sort_keys, **kwargs):
        super().__init__(*args, indent=2, sort_keys=True, **kwargs)


class FilmsdModelForm(forms.ModelForm):

    class Meta:
        model = FilmsdModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmsdModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id_kp:
            if 'id_kp' in self.fields:
                self.fields['id_kp'].help_text = format_html(f'''
                    Ссылка кинопоиска: <a href="
                    https://www.kinopoisk.ru/film/{self.instance.id_kp}"
                    target="_blank">
                    https://www.kinopoisk.ru/film/{self.instance.id_kp}</a>
                    <br>Ссылка на фильм:
                    <a href="/film/{self.instance.id_kp}/"
                    target="_blank">{self.instance.id_kp}</a>
                ''')
            if 'poster' in self.fields:
                image = self.instance.poster.split(',')
                self.fields['poster'].help_text = format_html(
                    f'<a href="{image[0]}" target="_blank">'
                    f'<img src="{image[1]}" alt="Image" '
                    f'style="max-height: 100px; max-width: 100px;"></a>'
                )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Записи в журнале"""
    list_display = (
        'action_time', 'user', 'content_type', 'object_repr', 'action_flag')
    list_filter = ('action_flag', 'user', 'content_type')
    search_fields = ('object_repr', 'change_message')
    list_per_page = settings.OBJECTS_PER_PAGE


class TorrentFileInline(admin.TabularInline):
    model = Torrent
    extra = 1  # Количество пустых форм
    verbose_name = "Торрент файл"
    verbose_name_plural = "Торрент файлы"


@admin.register(FilmsdModel)
class FilmsAdmin(admin.ModelAdmin):
    form = FilmsdModelForm
    inlines = [TorrentFileInline]
    list_display = (
        'image_preview',
        'id_kp',
        'name',
        'created_at',
        'is_published',
        'verified',
        'favorites_count'
    )
    list_display_links = ('name',)
    search_fields = ['name', 'id_kp']
    list_filter = ('is_published', 'verified')
    list_per_page = settings.OBJECTS_PER_PAGE
    actions = [is_published, not_is_published, verified, not_verified]
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget},
    }
    filter_horizontal = ('country', 'genres')

    @admin.display(description='В избранном')
    def favorites_count(self, obj):
        return obj.favorites_count

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

    def get_queryset(self, request):
        result = super().get_queryset(request)
        return result.annotate(
            favorites_count=Count('favorites'))


@admin.register(Coment)
class ComentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image_preview',
        'text',
        'author',
        'film_name',
        'created_at',
    )
    list_display_links = ('text',)
    list_per_page = settings.OBJECTS_PER_PAGE
    list_filter = ('author__username',)

    @admin.display(description='Название фильма')
    def film_name(self, obj):
        if obj.film:
            url = reverse('admin:films_filmsdmodel_change', args=[obj.film.id])
            return format_html(f'<a href="{url}">{obj.film.name}</a>')
        return 'Нет фильма'

    @admin.display(description='Постер')
    def image_preview(self, obj):
        """Показывать миниатюру изображения"""
        if obj.film:
            image = obj.film.poster.split(',')
            return mark_safe(
                f'<img src="{image[1]}" alt="Image" '
                f'style="max-height: 100px; max-width: 100px;"/>'
            )
        return 'Нет изображения'


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'film', 'created_at')
    list_per_page = settings.OBJECTS_PER_PAGE


@admin.register(Torrent)
class TorrentAdmin(admin.ModelAdmin):
    list_display = ('film',)
    list_per_page = settings.OBJECTS_PER_PAGE
