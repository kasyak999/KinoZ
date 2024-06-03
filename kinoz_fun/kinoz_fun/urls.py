from django.contrib import admin
from django.urls import path, include


app_name = 'kinoz_fun'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls'), name='index'),
    path('search/', include('search.urls'), name='search'),
    path('film/', include('films.urls'), name='films')
]
