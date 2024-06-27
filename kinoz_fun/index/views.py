from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpRequest
# Http404
from films.models import FilmsdModel

import json
from pprint import pprint


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница """
    # get_object_or_404
    results = get_list_or_404(FilmsdModel.objects.select_related(
        'cat').prefetch_related(
            'genres', 'country'
        ), is_published=True
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
