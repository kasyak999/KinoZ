from django.urls import path, reverse_lazy
from django.views.generic.edit import CreateView
from users.form import CustomUserCreationForm
from . import views


app_name = 'users'

urlpatterns = [
    path(
        'user/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=CustomUserCreationForm,
            success_url=reverse_lazy('login'),
        ),
        name='registration',
    ),

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
    path('message/', views.MessageListView.as_view(), name='message_list'),
    path(
        'message/<str:username>', views.MessageDetailView.as_view(),
        name='message_username'),
]
