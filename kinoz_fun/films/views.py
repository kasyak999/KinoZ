from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
# Http404
import requests
from pprint import pprint


# URL сервера API
api_url = "https://videocdn.tv/api/short"


def film(request: HttpRequest, kp: int) -> HttpResponse:
    """ страница фильма """
    # Параметры запроса
    data = {
        'kinopoisk_id': kp,
        'api_token': "fa6af878405af7b07dfe9f0d88ae421f",
    }
    # Отправка запроса POST с данными JSON
    response = requests.get(api_url, data)
    if response.json()['result']:
        context = {'result': response.json()['data'][0]}
        return render(request, 'films/film.html', context)
    raise Http404
