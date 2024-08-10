from typing import Any
from django.db.models.query import QuerySet
from django.views.generic import (
    DetailView, UpdateView, ListView, CreateView, DeleteView, TemplateView
)
from films.models import FilmsdModel
from django.shortcuts import get_object_or_404, redirect
from .api import information_film
from .form import AddFilmBaza
from django.http import HttpResponse, HttpRequest, Http404
import json
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError


OBJECTS_PER_PAGE = 10


class IndexListView(ListView):
    """Главная страница"""

    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = OBJECTS_PER_PAGE
    context_object_name = 'results'
    paginate_by = 5

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
        # except self.model.IntegrityError:
        #     raise Http404

    def get_object(self):
        return self.model.objects.get(
                id_kp=self.kwargs[self.pk_url_kwarg], verified=True,
                is_published=True
            )


class CreateFilm(CreateView):
    model = FilmsdModel
    template_name = 'films/add.html'
    form_class = AddFilmBaza

    @property
    def _result_api(self):
        return information_film(self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse('films:index')

    def get_initial(self):
        if self._result_api:
            return self._result_api
        else:
            initial = super().get_initial()
            initial['id_kp'] = self.kwargs[self.pk_url_kwarg]
            return initial

    def form_valid(self, form):
        if self._result_api:
            form.instance.id_kp = self.kwargs[self.pk_url_kwarg]
        else:
            form.instance.id_kp = self.kwargs[self.pk_url_kwarg]
        return super().form_valid(form)
