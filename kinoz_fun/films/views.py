from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, Http404
# Http404
import requests
from pprint import pprint
from . import key_name  # Импорт переменых и токенов для подключения к Api


def information_film(kp):
    """Собираем информацию о фильме"""
    data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN + str(kp)
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
    if response_kp.status_code == 200:
        response_kp = response_kp.json()
        pprint(response_kp)
        print('-----------------------')
        print(response_kp['type'])
        # print('-----------------------')
        if response_kp['type'] == 'FILM':
            cat = 'Фильм'
        elif response_kp['type'] == 'TV_SERIES':
            cat = 'Сериал'
        else:
            cat = response_kp['type']

        votecount = f"{response_kp['ratingKinopoiskVoteCount']:,}".replace(',', ' ')
        genres = ''
        for i in response_kp['genres']:
            for value in dict.values(i):
                genres += value + ', '
        country = ''
        for i in response_kp['countries']:
            for value in dict.values(i):
                country += value + ', '
        result = {
            'name': response_kp['nameRu'],
            'name_orig': response_kp['nameOriginal'],
            'year': response_kp['year'],
            'poster': response_kp['posterUrl'],
            'country': country[:-2],
            'genres': genres[:-2],
            'rating': response_kp['ratingKinopoisk'],
            'votecount': votecount,
            'description': response_kp['description'],
            'cat': cat,
            # 'name': response_kp['nameRu'],
            # 'name': response_kp['nameRu'],
            # 'name': response_kp['nameRu'],
            # 'name': response_kp['nameRu'],
        }
        return result
    raise Http404


def film(request: HttpRequest, kp: int) -> HttpResponse:
    """ страница фильма """
    # Параметры запроса
    data = {
        'kinopoisk_id': kp,
        'api_token': key_name.TOKEN,
    }
    response = requests.get(key_name.API_URL, data)
    if response.json()['result']:
        context = {
            'result': response.json()['data'][0],
            'result_kp': information_film(kp),
        }
        return render(request, 'films/film.html', context)
    raise Http404
