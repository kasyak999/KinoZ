from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'
urlpatterns = [
    path('user/<str:username>', views.PersonalAccount.as_view(), name='user'),
    path('user/email/', views.EmailUpdateView.as_view(), name='email_update'),
    path(
        'user/avatar/', views.AvatarUpdateView.as_view(),
        name='avatar_update'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
