from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Http404


def film(request: HttpRequest, kp: int) -> HttpResponse:
    """ страница фильма """
    context = {'id': kp}
    return render(request, 'films/film.html', context)
