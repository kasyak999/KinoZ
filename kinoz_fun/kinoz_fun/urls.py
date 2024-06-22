from django.contrib import admin
from django.urls import path, include
from django.conf import settings


app_name = 'kinoz_fun'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls'), name='index'),
    path('search/', include('search.urls'), name='search'),
    path('film/', include('films.urls'), name='films')
]

# Если проект запущен в режиме разработки...
if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
