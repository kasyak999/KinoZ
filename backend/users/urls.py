from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('users/', views.AllUsers.as_view(), name='user_list'),
    path('user/<str:username>', views.PersonalAccount.as_view(), name='user'),
    path(
        'user/<str:username>/edit/', views.EditAccountView.as_view(),
        name='edit_account'),
    path(
        'user/<str:username>/following/', views.FollowUserListView.as_view(),
        {'list_type': 'following'}, name='user_following'),
    path(
        'user/<str:username>/followers/', views.FollowUserListView.as_view(),
        {'list_type': 'followers'}, name='user_followers'),
]
