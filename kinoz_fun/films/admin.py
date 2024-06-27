from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country
# СategoriesModel
from django.utils.html import mark_safe
from django.urls import reverse


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
        'go_over'
    )
    list_display_links = ('poster_img',)
    list_filter = ('is_published', 'verified')
    search_fields = ['name']
    list_per_page = 10
    filter_horizontal = ('country', 'genres',)
    actions = ['on_published', 'off_published',
        'on_verified', 'off_verified'
    ]  # Действие

    @admin.action(description="Опубликовать")
    def on_published(modeladmin, request, queryset):
        queryset.update(is_published=True)

    @admin.action(description="Снять с публикации")
    def off_published(modeladmin, request, queryset):
        queryset.update(is_published=False)

    @admin.action(description="Проверено")
    def on_verified(modeladmin, request, queryset):
        queryset.update(verified=True)

    @admin.action(description="Не проверено")
    def off_verified(modeladmin, request, queryset):
        queryset.update(verified=False)

    def poster_img(self, obj):
        if obj.poster:
            obj.poster = obj.poster.split(', ')
            return mark_safe(
                f'<img src="{obj.poster[1]}" width="100" height="100">'
            )
        else:
            return "Пусто"

    def go_over(self, obj):
        url = reverse('films:film', args=[obj.id_kp])
        return mark_safe(
            f'<a href="{url}" target="_blank">перейти</a>'
        )

    poster_img.short_description = 'Постер'
    go_over.short_description = 'Ссылка на фильм'

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at',
    )


admin.site.register(FilmsdModel, FilmsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genres, CategoryAdmin)
admin.site.register(Country, CategoryAdmin)
