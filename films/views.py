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


OBJECTS_PER_PAGE = 10


class SearchView(ListView):
    """Поиск фильмов"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = OBJECTS_PER_PAGE

    def get_queryset(self):
        result = super().get_queryset()
        if self.request.GET.get('search'):
            result.filter(
                verified=True, is_published=True
            )
            return result.filter(
                Q(name__iregex=self.request.GET.get('search')) | 
                Q(name_orig__iregex=self.request.GET.get('search'))
            ).select_related('cat').prefetch_related('genres', 'country')
        else:
            return result.none()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['html_name'] = f'Поиск «{self.request.GET.get('search')}»'
            context['search'] = f'Найдено {self.object_list.count()}'
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
        # print(form)
        initial = self._result_api
        if initial:
            form.instance.poster = initial['poster']
            form.instance.scrinshot = initial['scrinshot']
            form.instance.rating = initial['rating']
            form.instance.votecount = initial['votecount']

        form.instance.id_kp = self.kwargs[self.pk_url_kwarg]
        result = FilmsdModel.objects.filter(
            id_kp=self.kwargs[self.pk_url_kwarg]
        )
        if result.count() > 0:
            print('уже есть')
            form.add_error(
                None,
                "Фильм с таким ID кинопоиска уже находится в базе на проверке."
            )
            return render(self.request, self.template_name, {'form': form})
        else:
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
