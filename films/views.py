from typing import Any
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView, TemplateView
)
from films.models import FilmsdModel, Coment
from django.shortcuts import get_object_or_404, redirect, render
from .api import information_film
from .form import AddFilmBaza, ComentForm
from django.http import HttpResponse, HttpRequest, Http404
from django.urls import reverse, reverse_lazy
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model


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
                    'films:add_film', kwargs={
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
        # pprint(initial['poster'])
        if not initial:
            initial = super().get_initial()
            initial['id_kp'] = self.kwargs[self.pk_url_kwarg]
        return initial

    def form_valid(self, form):
        initial = self._result_api
        if initial:
            form.instance.rating = initial['rating']
            form.instance.votecount = initial['votecount']
        form.instance.id_kp = self.kwargs[self.pk_url_kwarg]
        return super().form_valid(form)


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

    def get_object(self):
        return get_object_or_404(
            self.model, username=self.kwargs[self.pk_url_kwarg])

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.get_object()
        return context


def add_film(request):
    """Работа со сылкой кинопоиска"""
    template_name = 'films/add_kinopoisk.html'
    context = {}
    if request.method == 'POST':
        film_id = request.POST.get('film_id')
        result = film_id.split('/')
        if 'https:' in result:
            try:
                id_film = int(result[4])
            except (ValueError, TypeError):
                context['error'] = 'Неверный формат cсылки'
            else:  # если все ок
                return redirect('films:add_film_id', id_film)
        else:
            context['error'] = 'Ссылка на фильма не соответствует формату'
    return render(request, template_name, context)
