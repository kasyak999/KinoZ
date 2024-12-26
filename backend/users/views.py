from typing import Any
from django.views.generic import UpdateView, TemplateView, ListView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.conf import settings
from films.models import Coment
from .form import EmailUpdateForm, AvatarForm
from .models import Follow
from django.db.models import Prefetch
from django.db.models import F


User = get_user_model()


class PersonalAccount(LoginRequiredMixin, TemplateView):
    """Личный кабинет"""
    model = User
    template_name = 'users/user.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_object(self):
        user_profile = get_object_or_404(
            self.model, username=self.kwargs[self.pk_url_kwarg])
        return user_profile

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['user_profile'] = user_profile
        comment_all = Coment.objects.filter(
            author=context['user_profile'], film__verified=True,
            film__is_published=True).select_related('author', 'film')
        paginator = Paginator(comment_all, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['following'] = user_profile.follower.all().select_related(
            'following').count()
        context['follower'] = user_profile.following.all().select_related(
            'user').count()
        return context


class FollowUserListView(LoginRequiredMixin, ListView):
    """Подписан пользователь"""
    model = Follow
    template_name = 'users/follow.html'
    pk_url_kwarg = 'pk'
    paginate_by = settings.OBJECTS_PER_PAGE
    list_type_kwarg = 'list_type'

    def get_queryset(self):
        list_type = self.kwargs.get(self.list_type_kwarg)
        if list_type == 'following':
            return super().get_queryset().filter(
                user=self.kwargs[self.pk_url_kwarg]).select_related(
                'following', 'user')
        else:
            return super().get_queryset().filter(
                following=self.kwargs[self.pk_url_kwarg]).select_related(
                'following', 'user')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        list_type = self.kwargs.get(self.list_type_kwarg)
        if list_type == 'following':
            # context['object_list'] = self.get_followings_queryset()
            context['html_name'] = 'Подписки'
        else:
            # context['object_list'] = self.get_followers_queryset()
            context['html_name'] = 'Подписчики'
        context['list_type'] = list_type
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
