from typing import Any
from django.views.generic import ListView, FormView, UpdateView, DeleteView
from django.shortcuts import redirect
from django.db.models import Q, Count
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import url_has_allowed_host_and_scheme
from .api import information_film, search_film
from .form import (
    AddFilmBaza, ComentForm, AddFilmFavorites, FilmLinkForm, FormComment)
from .models import FilmsdModel, Genres, Category, Coment
from .mixin import OnlyAuthorMixin, FilmMixin, CommentMixin


User = get_user_model()


class SearchView(ListView):
    """Поиск фильмов"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = settings.OBJECTS_PER_PAGE

    def get_queryset(self):
        result = super().get_queryset().select_related(
            'cat'
        ).prefetch_related(
            'genres', 'country'
        )

        search_query = self.request.GET.get('search')
        genre_filter = self.request.GET.get('genre')
        category_filter = self.request.GET.get('categori')

        if search_query:
            return result.filter(
                verified=True, is_published=True
            ).filter(
                Q(name__iregex=search_query)
                | Q(name_orig__iregex=search_query)
                | Q(actors__iregex=search_query)
            )
        elif genre_filter or category_filter:
            filters = Q()
            if genre_filter:
                filters &= Q(genres__id=genre_filter)
            if category_filter:
                filters &= Q(cat_id=category_filter)

            return result.filter(filters)
        else:
            return self.model.objects.none()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['html_name'] = f'Поиск «{self.request.GET.get('search')}»'
            context['search'] = context['paginator'].count
            if context['paginator'].count == 0:
                context['search_kp'] = search_film(
                    self.request.GET.get('search'))
        else:
            context['html_name'] = 'Поиск'
            context['genres'] = Genres.objects.all()
            context['categories'] = Category.objects.all()
            context['selected_genre'] = self.request.GET.get('genre', '')
            context['selected_category'] = self.request.GET.get('categori', '')
        return context


class IndexListView(ListView):
    """Главная страница"""
    model = FilmsdModel
    template_name = 'films/index.html'
    paginate_by = settings.OBJECTS_PER_PAGE

    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            and self.kwargs.get('list_type') == 'favorite'
        ):
            # login_url = f"{reverse('login')}?next={self.request.path}"
            # return redirect(login_url)

            login_url = reverse('login')
            next_url = self.request.path
            if url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):  # Проверяем, является ли путь безопасным
                login_url = f"{login_url}?next={next_url}"
                return redirect(login_url)

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        result = super().get_queryset().filter(
            verified=True,
            is_published=True
        ).select_related('cat').prefetch_related('genres', 'country')

        if self.kwargs.get('list_type') == 'favorite':
            return result.filter(
                favorites__user=self.request.user
            ).prefetch_related('favorites')
        return result

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.kwargs.get('list_type') == 'favorite':
            context['html_name'] = 'Мое избранное'
        else:
            context['html_name'] = 'Главная страница'
        return context


class ComentView(ListView):
    """Все комментарии пользователей"""
    model = Coment
    template_name = 'films/coment_all_list.html'
    paginate_by = settings.OBJECTS_PER_PAGE


class DetailFilm(FilmMixin, ListView):
    """Пост подробнее"""
    model = FilmsdModel
    template_name = 'films/film.html'
    pk_url_kwarg = 'id_kp'
    paginate_by = settings.OBJECTS_PER_PAGE
    # success_url = reverse_lazy('birthday:list')

    @property
    def _result_api(self):
        rez = information_film(self.kwargs[self.pk_url_kwarg])
        return rez

    @property
    def get_film(self):
        return FilmsdModel.objects.annotate(
            comments_count=Count('coments', distinct=True),
            # is_favorite=Exists(Favorite.objects.filter(
            #     film=OuterRef('pk'), user=self.request.user)
            # )
        ).prefetch_related(
            'genres', 'country', 'torrents').select_related('cat').get(
            id_kp=self.kwargs[self.pk_url_kwarg], verified=True,
            is_published=True)

    def get_queryset(self):
        self.result = self.get_film
        return self.result.coments.all().select_related('author', 'film')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ComentForm()
        context['object'] = self.result
        context['len_coments'] = self.result.comments_count
        if self.request.user.is_authenticated:
            context['is_favorite'] = self.request.user.favorites.filter(
                film=self.result).exists()
        return context

    @method_decorator(login_required())
    def post(self, request, *args, **kwargs):
        """Добавление или удаление фильма из избранного"""
        film_id = self.kwargs[self.pk_url_kwarg]
        film = self.get_film

        # Обработка добавления/удаления фильма из избранного
        if 'favorite' in request.POST:
            result = request.user.favorites.filter(film=film)
            if result.exists():
                result.delete()
            else:
                form = AddFilmFavorites(data=request.POST)
                if form.is_valid():
                    form.save(user=request.user, film=film)

        # Обработка добавления комментария
        elif 'comment' in request.POST:
            form = ComentForm(data=request.POST)
            if form.is_valid():
                form.save(author=request.user, film=film)

        return redirect('films:film', id_kp=film_id)


class AddFilmView(FormView):
    """Добавление фильма с двумя этапами"""
    template_name = 'films/add_film.html'
    form_class = FilmLinkForm  # Форма для проверки ссылки
    second_form_class = AddFilmBaza  # форма для добавления фильма

    def get_context_data(self, **kwargs):
        """Контекст для отображения формы"""
        context = super().get_context_data(**kwargs)
        context['is_second_form'] = kwargs.get('is_second_form', False)
        return context

    def form_valid(self, form):
        """Обработка валидной первой формы"""
        film_id = form.cleaned_data['film_id']
        return self.load_film_data(film_id, self.request)

    def post(self, request, *args, **kwargs):
        """Обработка отправки форм"""
        # Если пришёл POST-запрос на основную форму
        if 'is_second_form' in request.POST:
            second_form = self.second_form_class(request.POST)
            if second_form.is_valid():
                second_form.save()
                messages.success(
                    request, 'Фильм успешно добавлен в базу, '
                    'после проверки он будет доступен')
                return redirect(reverse_lazy('films:add_film'))
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """Обработка GET-запроса для получения id фильма и загрузки данных"""
        film_id = request.GET.get('id')
        if film_id:
            return self.load_film_data(film_id, request)
        return self.render_to_response(self.get_context_data())

    def load_film_data(self, film_id, request):
        """Загрузка данных фильма"""
        film_data = information_film(film_id, request)
        if film_data:
            return self.render_to_response(
                self.get_context_data(
                    form=self.second_form_class(initial=film_data),
                    is_second_form=True
                )
            )
        return self.render_to_response(self.get_context_data())


class ComentUpdateView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, UpdateView
):
    """Изменение комментария"""
    form_class = FormComment


class CommentDeleteView(
    LoginRequiredMixin, OnlyAuthorMixin, CommentMixin, DeleteView
):
    """Удаление коментария"""
