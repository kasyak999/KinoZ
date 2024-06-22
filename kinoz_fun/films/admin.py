from django.contrib import admin
from . models import FilmsdModel
from django.utils.html import mark_safe


class FilmsAdmin(admin.ModelAdmin):
    list_display = (
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


admin.site.register(FilmsdModel, FilmsAdmin)
