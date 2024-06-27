from django.urls import path
from . import views


app_name = 'index'
urlpatterns = [
    path('', views.index, name='index'),
    path('contacts/', views.contacts, name='contacts'),
    # path('add_country/', views.add_country, name='country'),
    # path('add_genres/', views.add_genres, name='genres')
]
