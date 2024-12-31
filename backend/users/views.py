from typing import Any
from django.views.generic import UpdateView, ListView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count
from .form import EmailUpdateForm, AvatarForm, AddFollow


User = get_user_model()


class PersonalAccount(LoginRequiredMixin, ListView):
    """Личный кабинет"""
    template_name = 'users/user.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE
    form_class = AddFollow

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User.objects.annotate(
                following_count=Count('followers', distinct=True),
                follower_count=Count('followings', distinct=True),
                comments_count=Count('coments', distinct=True)
            ).prefetch_related('coments__author', 'coments__film'),
            username=self.kwargs[self.pk_url_kwarg]
        )
        return self.user_profile.coments.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        context['following'] = self.user_profile.following_count
        context['follower'] = self.user_profile.follower_count
        context['len_coments'] = self.user_profile.comments_count
        if self.request.user.is_authenticated:
            context['is_follow'] = self.user_profile.followings.filter(
                user=self.request.user).exists()
        return context

    def post(self, request, *args, **kwargs):
        """Добавление или удаление фильма из избранного"""
        username = self.kwargs[self.pk_url_kwarg]
        self.get_queryset()
        result = self.user_profile.followings.filter(user=request.user)
        if not result.exists():
            form_data = {
                'user': request.user,
                'following': self.user_profile
            }
            form = self.form_class(data=form_data)
            if form.is_valid():
                form.save()
        else:
            result.delete()
        return redirect('users:user', username=username)


class FollowUserListView(LoginRequiredMixin, ListView):
    """Подписан пользователь"""
    template_name = 'users/follow.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE
    list_type = 'list_type'

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User.objects.annotate(
                following_count=Count('followers', distinct=True),
                follower_count=Count('followings', distinct=True),
                # ).prefetch_related(

                #     # 'followers__user',
                #     # 'followings__following',
                # ),
            ), username=self.kwargs[self.pk_url_kwarg]
        )
        list_type = self.kwargs.get(self.list_type)
        if list_type == 'following':
            return self.user_profile.followers.all().select_related(
                'following', 'user')
        return self.user_profile.followings.all().select_related(
            'following', 'user')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        if self.kwargs.get(self.list_type) == 'following':
            context['follow_count'] = self.user_profile.follower_count
        else:
            context['follow_count'] = self.user_profile.following_count
        return context


class UserUpdateBaseView(LoginRequiredMixin, UpdateView):
    """Базовый класс для обновления данных пользователя"""

    def get_success_url(self):
        return reverse(
            'users:user', kwargs={'username': self.request.user.username})

    def get_object(self):
        return self.request.user


class EmailUpdateView(UserUpdateBaseView):
    """Изменение email пользователя"""
    model = User
    form_class = EmailUpdateForm
    template_name = 'registration/email_update.html'


class AvatarUpdateView(UserUpdateBaseView):
    """Изменение аватар пользователя"""
    model = User
    form_class = AvatarForm
    template_name = 'users/avatar.html'


def page_not_found(request, exception):
    """страницы 404"""
    return render(request, 'users/404.html', status=404)
