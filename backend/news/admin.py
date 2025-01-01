from django.contrib import admin
from django.conf import settings
from .models import EventUser


@admin.register(EventUser)
class ComentAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'event',
        'user',
        'created_at',
    )
    list_display_links = ('user',)
    list_per_page = settings.OBJECTS_PER_PAGE
