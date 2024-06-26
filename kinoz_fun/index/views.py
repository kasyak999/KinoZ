from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Http404
from films.models import FilmsdModel, Genres, Country
import json
from pprint import pprint


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница """
    results = FilmsdModel.objects.filter(
        is_published=True).select_related('cat').prefetch_related(
            'genres', 'country'
        )
    context = {
        'html_title': 'Гланвая страница',
        'html_name': 'Главная',
        'results': results,
        # 'results': [i for i in range(666, 670)],
    }
    return render(request, 'index/index.html', context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Страница контакты"""
    context = {
        'title': 'Контакты',
    }
    return render(request, 'index/contacts.html', context)
