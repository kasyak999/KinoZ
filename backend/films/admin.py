from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country, Coment
from django.utils.html import format_html
from django import forms
from django.db.models import Count


class FilmsdModelForm(forms.ModelForm):
    class Meta:
        model = FilmsdModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(FilmsdModelForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.id_kp:
            self.fields['id_kp'].help_text = format_html(
                f'''ссылка кинопоиска:
                <a href="https://www.kinopoisk.ru/film/{self.instance.id_kp}"
                target="_blank">https://www.kinopoisk.ru/film/{self.instance.id_kp}</a>
                <br>ссылка на фильм:
                <a href="/film/{self.instance.id_kp}/"
                target="_blank">{self.instance.id_kp}</a>
                '''
            )


class FilmsAdmin(admin.ModelAdmin):
    form = FilmsdModelForm
    list_display = (
        'id_kp',
        'name',
        'is_published',
        'verified'
    )
    list_display_links = ('name',)
    search_fields = ['name', 'id_kp']
    list_filter = ('is_published', 'verified')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'films_count',  # Добавьте поле product_count
    )
    list_display_links = ('name',)
    search_fields = ['name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Аннотируем количество связанных фильмов для каждой категории
        return queryset.annotate(films_count=Count('posts'))

    def films_count(self, obj):
        """Выводит количество записей в FilmsdModel, связанных с категорией."""
        return obj.films_count

    films_count.short_description = ('Количество фильмов')


class ComentAdmin(admin.ModelAdmin):
    list_display = (
        'text',
        'get_film_name'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('film')

    def get_film_name(self, obj):
        return obj.film.name

    get_film_name.short_description = 'Название фильма'  # Переопределяем verbose_name для столбца


admin.site.register(FilmsdModel, FilmsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genres, admin.ModelAdmin)
admin.site.register(Country, admin.ModelAdmin)
admin.site.register(Coment, ComentAdmin)
