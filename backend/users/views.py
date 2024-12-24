from typing import Any
from django.views.generic import UpdateView, TemplateView
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.conf import settings
from films.models import Coment
from .form import EmailUpdateForm, AvatarForm


User = get_user_model()


class PersonalAccount(LoginRequiredMixin, TemplateView):
    """Личный кабинет"""
    model = User
    template_name = 'users/user.html'
    pk_url_kwarg = 'username'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_object(self):
        return get_object_or_404(
            self.model, username=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['user_profile'] = user_profile
        comment_all = Coment.objects.filter(
            author=user_profile, film__verified=True, film__is_published=True
        ).select_related('author', 'film')
        paginator = Paginator(comment_all, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


class EmailUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение email пользователя"""
    model = User
    form_class = EmailUpdateForm
    template_name = 'registration/email_update.html'

    def get_success_url(self):
        return reverse('users:user', kwargs={'username': self.request.user})

    def get_object(self):
        return self.request.user


class AvatarUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение аватар пользователя"""
    model = User
    form_class = AvatarForm
    template_name = 'users/avatar.html'

    def get_success_url(self):
        return reverse('users:user', kwargs={'username': self.request.user})

    def get_object(self):
        return self.request.user


def page_not_found(request, exception):
    """страницы 404"""
    return render(request, 'users/404.html', status=404)
