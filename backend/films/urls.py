from django.urls import path
from . import views


app_name = 'films'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path(
        'favorite/', views.IndexListView.as_view(),
        {'list_type': 'favorite'}, name='favorite'),
    path('film/<int:id_kp>/', views.DetailFilm.as_view(), name='film'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add_film/', views.AddFilmView.as_view(), name='add_film'),
]
