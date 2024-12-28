from django.urls import path
from . import views


app_name = 'films'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('film/<int:id_kp>/', views.DetailFilm.as_view(), name='film'),
    path('add_film', views.add_film, name='add_film'),
    path('add_film/<int:pk>/', views.CreateFilm.as_view(), name='add_film_id'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('film/favorite/', views.FavoriteListView.as_view(), name='favorite'),
]
