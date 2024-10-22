from typing import Any
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView, TemplateView
)
from films.models import FilmsdModel, Coment
from django.shortcuts import get_object_or_404, redirect, render
from .api import information_film
from .form import AddFilmBaza, ComentForm, EmailUpdateForm
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse, reverse_lazy
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib import messages


User = get_user_model()
OBJECTS_PER_PAGE = 10


class SearchView(ListView):
    """Поиск фильмов"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        result = super().get_queryset()
        if self.request.GET.get('search'):
            return result.filter(
                verified=True, is_published=True
            ).filter(
                Q(name__iregex=self.request.GET.get('search')) |
                Q(name_orig__iregex=self.request.GET.get('search'))
            ).select_related('cat').prefetch_related('genres', 'country')
        else:
            return result.none()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['html_name'] = f'Поиск «{self.request.GET.get('search')}»'
            context['search'] = self.object_list.count()
        else:
            context['html_name'] = 'Поиск'
        context['html_title'] = context['html_name']
        return context


class IndexListView(ListView):
    """Главная страница"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        return super().get_queryset().filter(
            verified=True,
            is_published=True
        ).select_related('cat').prefetch_related('genres', 'country')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['html_name'] = 'Главная страница'
        context['html_title'] = context['html_name']
        return context


class DetailFilm(DetailView):
    """Пост подробнее"""
    model = FilmsdModel
    template_name = 'films/film.html'
    pk_url_kwarg = 'id_kp'
    paginate_by = OBJECTS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return redirect(
                reverse(
                    'films:add_film_id', kwargs={
                        'pk': self.kwargs[self.pk_url_kwarg]
                    }
                )
            )

    def get_object(self):
        return self.model.objects.prefetch_related('genres', 'country').get(
                id_kp=self.kwargs[self.pk_url_kwarg], verified=True,
                is_published=True
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentForm()
        comment_all = self.object.coment.select_related('author')
        paginator = Paginator(comment_all, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class CreateFilm(CreateView):
    """Добавление нового фильма"""
    model = FilmsdModel
    template_name = 'films/add.html'
    form_class = AddFilmBaza

    @property
    def _result_api(self):
        rez = information_film(self.kwargs[self.pk_url_kwarg])
        return rez

    def get_success_url(self):
        return reverse('films:index')

    def get_initial(self):
        initial = self._result_api
        if initial:
            return initial
        return super().get_initial()

    def get(self, request, *args, **kwargs):
        # Проверяем, существует ли фильм
        if self._result_api is None:
            messages.error(request, 'Такой фильм уже есть в базе')
            return redirect('films:add_film')
            # context = {'error': 'Такой фильм уже есть в базе'}
            # return render(
            #     request, 'films/add_kinopoisk.html', context)
        return super().get(request, *args, **kwargs)


class AddComment(LoginRequiredMixin, CreateView):
    """Новый комментарий"""
    model = Coment
    template_name = 'films/add_coment.html'
    form_class = ComentForm

    @property
    def _id_kp(self):
        rez = FilmsdModel.objects.get(id=self.kwargs[self.pk_url_kwarg])
        return rez

    def get_success_url(self):
        return reverse('films:film', kwargs={
            'id_kp': self._id_kp.id_kp
        })

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.film = self._id_kp
        return super().form_valid(form)


class personal_account(LoginRequiredMixin, TemplateView):
    """Личный кабинет"""
    model = User
    template_name = 'films/user.html'
    pk_url_kwarg = 'username'
    paginate_by = OBJECTS_PER_PAGE

    def get_object(self):
        return get_object_or_404(
            self.model, username=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object()
        context['user_profile'] = user_profile
        comment_all = Coment.objects.filter(
            author=user_profile).select_related('author', 'film')
        paginator = Paginator(comment_all, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

        return context


def add_film(request):
    """Работа со сылкой кинопоиска"""
    template_name = 'films/add_kinopoisk.html'
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
        result = film_id.split('/')
        if 'https:' in result:
            try:
                id_film = int(result[4])
            except (ValueError, TypeError, IndexError):
                messages.error(request, 'Неверный формат cсылки')
            else:  # если все ок
                bd = FilmsdModel.objects.filter(id_kp=id_film)
                if not bd:
                    return redirect('films:add_film_id', id_film)
                messages.error(request, 'Такой фильм уже есть в базе')
        else:
            messages.error(
                request, 'Ссылка на фильма не соответствует формату')
    return render(request, template_name)


class EmailUpdateView(LoginRequiredMixin, UpdateView):
    """Изменение email пользователя"""
    model = User
    form_class = EmailUpdateForm
    template_name = 'registration/email_update.html'

    def get_success_url(self):
        return reverse('user', kwargs={'username': self.request.user})

    def get_object(self):
        return self.request.user  # Получаем текущего пользователя
