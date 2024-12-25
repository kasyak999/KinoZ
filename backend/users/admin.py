from django.contrib import admin
from django.contrib.auth import get_user_model
# from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import Follow


User = get_user_model()


@admin.register(User)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'image_preview')
    search_fields = ('email', 'username')
    list_display_links = ('username',)

    @admin.display(description='Аватар')
    def image_preview(self, obj):
        """Показывать миниатюру изображения"""
        if obj.avatar:
            return mark_safe(
                f'<img src="{obj.avatar.url}" alt="Image" '
                f'style="max-height: 100px; max-width: 100px;"/>'
            )
        return 'Нет изображения'


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')
    search_fields = ('username',)
    list_display_links = ('user',)
