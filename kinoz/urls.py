from django.contrib import admin
from django.urls import path, include
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('films.urls')),
    path('user/', include('django.contrib.auth.urls')),
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
