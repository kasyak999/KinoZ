from typing import Any
from django.views.generic import UpdateView, ListView, CreateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count, Q
from django.urls import reverse_lazy, reverse
from .form import AddFollow, EditUserForm, MessageForm
from .models import Message


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
        """Добавление или удаление подписчика"""
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


class EditAccountView(LoginRequiredMixin, UpdateView):
    """Редактирование учетной записи пользователя"""
    model = User
    template_name = 'users/edit_account.html'
    form_class = EditUserForm

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy(
            'users:user', kwargs={'username': self.request.user.username})


class FollowUserListView(LoginRequiredMixin, ListView):
    """Подписан пользователь"""
    template_name = 'users/follow.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE * 2

    def get_queryset(self):
        self.user_profile = get_object_or_404(
            User.objects.annotate(
                following_count=Count('followers', distinct=True),
                follower_count=Count('followings', distinct=True),
            ), username=self.kwargs[self.pk_url_kwarg]
        )
        if self.kwargs.get('list_type') == 'following':
            result = self.user_profile.followers.all().select_related(
                'following', 'user')
        else:
            result = self.user_profile.followings.all().select_related(
                'following', 'user')

        search = self.request.GET.get('search')
        if search:
            result = result.filter(
                Q(following__username__icontains=search)
                | Q(user__username__icontains=search)
            )
        return result

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.user_profile
        if self.kwargs.get('list_type') == 'following':
            context['follow_count'] = self.user_profile.following_count
        else:
            context['follow_count'] = self.user_profile.follower_count
        return context


class AllUsers(ListView):
    """Список всех пользователей и поиск"""
    model = User
    template_name = 'users/all_users.html'
    paginate_by = settings.OBJECTS_PER_PAGE * 2

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(username__icontains=query)
        return queryset


class MessageListView(LoginRequiredMixin, ListView):
    """Список всех сообщений"""
    model = User
    template_name = 'users/message_list.html'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_queryset(self):
        queryset = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related('sender', 'receiver')

        queryset.filter(
            receiver=self.request.user, is_read=False).update(is_read=True)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['messages'] = None
        return context


class MessageDetailView(LoginRequiredMixin, CreateView):
    """Отправить сообщение"""
    model = Message
    template_name = 'users/message_form.html'
    form_class = MessageForm
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_form(self, form_class=None):
        """Устанавливаем sender и receiver перед валидацией"""
        form = super().get_form(form_class)
        form.instance.sender = self.request.user
        receiver = get_object_or_404(
            User,
            username=self.kwargs[self.pk_url_kwarg]
        )
        form.instance.receiver = receiver
        return form

    def get_success_url(self):
        return reverse('users:message_list')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['recipient'] = self.kwargs[self.pk_url_kwarg]
        return context
