from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Http404


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница поиска"""
    return render(request, 'search/index.html')
