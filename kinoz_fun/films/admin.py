from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country
# СategoriesModel
from django.utils.html import mark_safe


class FilmsAdmin(admin.ModelAdmin):
    list_display = (
        'id_kp',
        'poster_img',
        'name',
        'year',
        'is_published',
        'created_at',
    )
    list_display_links = ('poster_img',)
    list_filter = ('is_published',)
    search_fields = ['name']
    list_per_page = 10

    def poster_img(self, obj):
        if obj.poster:
            return mark_safe(f'<img src="{obj.poster}" width="100" height="100">')
        else:
            return "No poster"

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
