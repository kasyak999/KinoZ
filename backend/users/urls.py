from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('user/<str:username>', views.PersonalAccount.as_view(), name='user'),
    path('user/email/', views.EmailUpdateView.as_view(), name='email_update'),
    path(
        'user/avatar/', views.AvatarUpdateView.as_view(),
        name='avatar_update'),
    path(
        'users/<str:username>/following/', views.FollowUserListView.as_view(),
        {'list_type': 'following'}, name='user_following'),
    path(
        'users/<str:username>/followers/', views.FollowUserListView.as_view(),
        {'list_type': 'followers'}, name='user_followers'),
]
