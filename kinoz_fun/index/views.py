from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Http404


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница """
    context = {
        'title': 'Гланвая страница',
        'name': 'Главная',
        'film_array': [i for i in range(15)],
    }
    return render(request, 'index/index.html', context)
