from django.urls import path
from . import views


app_name = 'films'
urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    path('film/<int:id_kp>/', views.DetailFilm.as_view(), name='film'),
    path('add_film/<int:pk>/', views.CreateFilm.as_view(), name='add_film'),
    path('comment/<int:pk>/', views.AddComment.as_view(), name='add_comment'),
]