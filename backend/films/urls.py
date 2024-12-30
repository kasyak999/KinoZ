from django.urls import path
from . import views


app_name = 'films'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('film/<int:id_kp>/', views.DetailFilm.as_view(), name='film'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('film/favorite/', views.FavoriteListView.as_view(), name='favorite'),
    path('add_film/', views.AddFilmView.as_view(), name='add_film'),
]
