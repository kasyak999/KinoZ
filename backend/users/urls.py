from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('user/<str:username>', views.PersonalAccount.as_view(), name='user'),
    path('user/email/', views.EmailUpdateView.as_view(), name='email_update'),
]
