from django.urls import path
from . import views


app_name = 'films'
urlpatterns = [
    path('<int:kp>/', views.film, name='film'),
]
