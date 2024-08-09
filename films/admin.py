from django.contrib import admin
from . models import FilmsdModel, Category, Genres, Country


admin.site.register(FilmsdModel, admin.ModelAdmin)
admin.site.register(Category, admin.ModelAdmin)
admin.site.register(Genres, admin.ModelAdmin)
admin.site.register(Country, admin.ModelAdmin)
