from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country
# СategoriesModel
from django.utils.html import mark_safe


admin.site.empty_value_display = 'Не задано'


class FilmsAdmin(admin.ModelAdmin):
    list_display = (
        'id_kp',
        'poster_img',
        'name',
        'year',
        'is_published',
        'verified',
        'created_at',
    )
    list_display_links = ('poster_img',)
    list_filter = ('is_published', 'verified')
    search_fields = ['name']
    list_per_page = 10
    filter_horizontal = ('country', 'genres',)

    def poster_img(self, obj):
        if obj.poster:
            obj.poster = obj.poster.split(', ')
            return mark_safe(
                f'<img src="{obj.poster[1]}" width="100" height="100">'
            )
        else:
            return "Пусто"

    poster_img.short_description = 'poster'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'created_at',
    )


admin.site.register(FilmsdModel, FilmsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genres, CategoryAdmin)
admin.site.register(Country, CategoryAdmin)
