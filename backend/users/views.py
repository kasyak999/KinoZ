from typing import Any
from django.views.generic import UpdateView, TemplateView, ListView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from films.models import Coment
from .form import EmailUpdateForm, AvatarForm
from .models import Follow
from django.db.models import Count


User = get_user_model()


class PersonalAccount(LoginRequiredMixin, ListView):
    """Личный кабинет"""
    template_name = 'users/user.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE

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
        return context


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
        related_name = (
            'followers' if list_type == 'following' else 'followings')
        return getattr(self.user_profile, related_name).select_related(
            'following', 'user'
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        context['following'] = self.user_profile.following_count
        context['follower'] = self.user_profile.follower_count
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
