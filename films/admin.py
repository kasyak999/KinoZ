from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country


class FilmsAdmin(admin.ModelAdmin):
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

    def films_count(self, obj):
        """Выводит количество записей в FilmsdModel, связанных с категорией."""
        return obj.posts.count()  # Используйте filmsdmodel_set для связи

    films_count.short_description = ('Количество фильмов')


admin.site.register(FilmsdModel, FilmsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genres, admin.ModelAdmin)
admin.site.register(Country, admin.ModelAdmin)
