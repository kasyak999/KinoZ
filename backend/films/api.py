import os
from django.http import Http404
from dotenv import load_dotenv
import requests
from .models import FilmsdModel


load_dotenv()
KINOPOISK_URL = 'https://kinopoiskapiunofficial.tech'
# Апи кинопоиска
KINOPOISK_URL_MAIN = '/api/v2.2/films/'
# Добавочный адрес
DATA_KP = {  # Параметры запроса к кинопоиску
    'X-API-KEY': os.getenv('KINOPOISK_API_KEY'),
    'Content-Type': 'application/json'
}


def search_film(value, id_kp):
    """Поиск фильма"""
    data_kp = KINOPOISK_URL + '/api/v2.1/films/search-by-keyword'
    response_kp = requests.get(
        data_kp, headers=DATA_KP, params={'keyword': value})
    # print(response_kp)
    if response_kp.status_code == 200:
        response_kp = response_kp.json()
        result = []
        for i in response_kp['films']:
            if not i['filmId'] in id_kp:
                result.append(i)
        return result
    else:
        print('Ошибка в базе кинопоиска')


def add_scrinshot_film(data_kp):
    """Добавление кадров из фильма с кинопоиска"""
    data_kp += '/images'
    response_kp = requests.get(data_kp, headers=DATA_KP)
    if response_kp.status_code == 200:
        scrinshot = response_kp.json()['items']
        # print('--------------------------------------')
        # print(scrinshot)
        # print('--------------------------------------')
        return scrinshot


def information_film(kp: int):
    result = FilmsdModel.objects.filter(id_kp=kp).exists()
    if not result:
        return connection_api(kp)


def connection_api(kp: int):
    """Собираем информацию о фильме из кинопоиска"""
    data_kp = KINOPOISK_URL + KINOPOISK_URL_MAIN + str(kp)
    response_kp = requests.get(data_kp, headers=DATA_KP)
    # print(response_kp)
    if response_kp.status_code == 200:
        scrinshot = add_scrinshot_film(data_kp)
        response_kp = response_kp.json()
        # pprint(response_kp)
        if response_kp['type'] == 'FILM':
            cat = 'Фильм'
        elif response_kp['type'] == 'TV_SERIES':
            cat = 'Сериал'
        else:
            cat = response_kp['type']

        genres = [list(i.values())[0] for i in response_kp['genres']]
        # print(genres)
        genres = ', '.join(genres)
        country = [list(dict.values(i))[0] for i in response_kp['countries']]
        country = ', '.join(country)
        result = {
            'id_kp': response_kp['kinopoiskId'],
            'name': response_kp['nameRu'],
            'name_orig': response_kp['nameOriginal'],
            'year': response_kp['year'],
            'poster': (
                f"{response_kp['posterUrl']}, "
                f"{response_kp['posterUrlPreview']}"
            ),
            'country': country,
            'genres': genres,
            'rating': response_kp['ratingKinopoisk'],
            'votecount': response_kp['ratingKinopoiskVoteCount'],
            'description': response_kp['description'],
            'cat': cat,
            'scrinshot': scrinshot,
        }
        return result
    # raise Http404
    else:
        raise Http404
