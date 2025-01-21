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

    path(
        'film/<film_id_kp>/edit_comment/<comment_id>/',
        views.ComentUpdateView.as_view(), name='edit_comment'
    ),
    path(
        'film/<film_id_kp>/delete_comment/<comment_id>/',
        views.CommentDeleteView.as_view(), name='delete_comment'
    ),
    path('coment_all/', views.ComentView.as_view(), name='coment_all_list'),

]
