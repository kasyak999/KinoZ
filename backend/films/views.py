from typing import Any
from django.views.generic import DetailView, ListView, CreateView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from .api import information_film
from .form import AddFilmBaza, ComentForm
from .models import FilmsdModel, Coment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count


User = get_user_model()


class SearchView(ListView):
    """Поиск фильмов"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_queryset(self):
        result = super().get_queryset()
        if self.request.GET.get('search'):
            return result.filter(
                verified=True, is_published=True
            ).filter(
                Q(name__iregex=self.request.GET.get('search'))
                | Q(name_orig__iregex=self.request.GET.get('search'))
            ).select_related('cat').prefetch_related('genres', 'country')
        else:
            return result.none()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['html_name'] = f'Поиск «{self.request.GET.get('search')}»'
            context['search'] = self.get_queryset().count()
        else:
            context['html_name'] = 'Поиск'
        context['html_title'] = context['html_name']
        return context


class IndexListView(ListView):
    """Главная страница"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = settings.OBJECTS_PER_PAGE

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


class DetailFilm(ListView):
    """Пост подробнее"""
    model = FilmsdModel
    template_name = 'films/film.html'
    pk_url_kwarg = 'id_kp'
    paginate_by = settings.OBJECTS_PER_PAGE

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

    def get_queryset(self):
        self.result = FilmsdModel.objects.annotate(
            comments_count=Count('coments', distinct=True)
        ).prefetch_related(
            'genres', 'country').select_related('cat').get(
            id_kp=self.kwargs[self.pk_url_kwarg], verified=True,
            is_published=True
        )
        return self.result.coments.all().select_related('author', 'film')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentForm()
        context['object'] = self.result
        context['len_coments'] = self.result.comments_count

        if self.request.user.is_authenticated:
            context['is_favorite'] = context['object'].favorites.filter(
                user=self.request.user).exists()
        return context
    
    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        """Добавление или удаление фильма из избранного"""
        film = self.result
        print('-----------------------------', film)
        if film.favorites.filter(user=request.user).exists():
            film.favorites.filter(user=request.user).delete()
        else:
            film.favorites.create(user=request.user, recipe=film)
        return redirect('films:film', id_kp=film.id_kp)


# class DetailFilm(DetailView):
#     """Пост подробнее"""
#     model = FilmsdModel
#     template_name = 'films/film.html'
#     pk_url_kwarg = 'id_kp'
#     paginate_by = settings.OBJECTS_PER_PAGE

#     def dispatch(self, request, *args, **kwargs):
#         try:
#             return super().dispatch(request, *args, **kwargs)
#         except self.model.DoesNotExist:
#             return redirect(
#                 reverse(
#                     'films:add_film_id', kwargs={
#                         'pk': self.kwargs[self.pk_url_kwarg]
#                     }
#                 )
#             )

#     def get_object(self):
#         return self.model.objects.prefetch_related('genres', 'country').get(
#             id_kp=self.kwargs[self.pk_url_kwarg], verified=True,
#             is_published=True
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['form'] = ComentForm()
#         comment_all = self.object.coments.select_related('author', 'film')
#         paginator = Paginator(comment_all, self.paginate_by)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context['page_obj'] = page_obj

#         if self.request.user.is_authenticated:
#             context['is_favorite'] = context['object'].favorites.filter(
#                 user=self.request.user).exists()
#         return context

#     @method_decorator(login_required())
#     def post(self, request, *args, **kwargs):
#         """Добавление или удаление фильма из избранного"""
#         film = self.get_object()
#         if film.favorites.filter(user=request.user).exists():
#             film.favorites.filter(user=request.user).delete()
#         else:
#             film.favorites.create(user=request.user, recipe=film)
#         return redirect('films:film', id_kp=film.id_kp)


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
        messages.success(
            self.request,
            'Фильм успешно добавлен в базу, после проверки он будет доступен')
        return reverse('films:add_film')

    def get_initial(self):
        initial = self._result_api
        if initial:
            return initial
        return super().get_initial()


class AddComment(LoginRequiredMixin, CreateView):
    """Новый комментарий"""
    model = Coment
    template_name = 'films/add_coment.html'
    form_class = ComentForm

    @property
    def _id_kp(self):
        return FilmsdModel.objects.get(id=self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        return reverse('films:film', kwargs={'id_kp': self._id_kp.id_kp})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.film = self._id_kp
        return super().form_valid(form)


def add_film(request):
    """Работа с сылкой кинопоиска"""
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


class FavoriteListView(LoginRequiredMixin, ListView):
    """Список избранных фильмов пользователя"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_queryset(self):
        return FilmsdModel.objects.filter(
            favorites__user=self.request.user,
            verified=True,
            is_published=True
        ).prefetch_related('favorites', 'genres', 'country')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['html_name'] = 'Мое избранное'
        context['html_title'] = context['html_name']
        return context
