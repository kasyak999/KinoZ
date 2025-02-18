import os
from django.http import Http404
from django.contrib import messages
from dotenv import load_dotenv
import requests
from .models import FilmsdModel
# from pprint import pprint


load_dotenv()
KINOPOISK_URL = 'https://kinopoiskapiunofficial.tech'
# Апи кинопоиска
KINOPOISK_URL_MAIN = '/api/v2.2/films/'
# Добавочный адрес
DATA_KP = {  # Параметры запроса к кинопоиску
    'X-API-KEY': os.getenv('KINOPOISK_API_KEY'),
    'Content-Type': 'application/json'
}


# /api/v2.2/films/{id}/videos
def trailer_film(value):
    """трейлеры к фильму"""
    data_kp = KINOPOISK_URL + f'/api/v2.2/films/{value}/videos'
    response_kp = requests.get(
        data_kp, headers=DATA_KP)
    # print(response_kp)
    if response_kp.status_code == 200:
        response_kp = response_kp.json()
        # pprint(response_kp)
        return response_kp['items']
    else:
        print('Ошибка в базе кинопоиска')


# /api/v1/staff?filmId=666
def actors_film(value):
    """актеры для фильма"""
    data_kp = KINOPOISK_URL + '/api/v1/staff'
    response_kp = requests.get(
        data_kp, headers=DATA_KP, params={'filmId': value})
    # print(response_kp)
    if response_kp.status_code == 200:
        response_kp = response_kp.json()

        professions_dict = {}
        for profession in response_kp:
            if profession['professionText'] not in professions_dict:
                professions_dict[profession['professionText']] = []

            professions_dict[profession['professionText']].append(
                profession['nameRu'])
        return professions_dict
    else:
        print('Ошибка в базе кинопоиска')


def search_film(value):
    """Поиск фильма, пока не используется"""
    data_kp = KINOPOISK_URL + '/api/v2.1/films/search-by-keyword'
    response_kp = requests.get(
        data_kp, headers=DATA_KP, params={'keyword': value})
    # print(response_kp)
    if response_kp.status_code == 200:
        response_kp = response_kp.json()

        result_kp = [film for film in response_kp['films']]
        filmId = [filmId['filmId'] for filmId in result_kp]
        existing_ids = set(FilmsdModel.objects.filter(
            id_kp__in=filmId).values_list('id_kp', flat=True))

        for key, value in enumerate(result_kp):
            if value['filmId'] in existing_ids:
                result_kp[key] = None

        # Убираем все элементы, которые равны None
        result_kp = [film for film in result_kp if film is not None]
        return result_kp
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


def information_film(kp: int, request=None):
    result = FilmsdModel.objects.filter(id_kp=kp).exists()
    if not result:
        return connection_api(kp)
    return messages.error(request, 'Фильм уже существует в базе.')


def connection_api(kp: int):
    """Собираем информацию о фильме из кинопоиска"""
    data_kp = KINOPOISK_URL + KINOPOISK_URL_MAIN + str(kp)
    response_kp = requests.get(data_kp, headers=DATA_KP)
    # print(response_kp)
    if response_kp.status_code == 200:
        # actors = actors_film(kp)
        # scrinshot = add_scrinshot_film(data_kp)
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
            'scrinshot': add_scrinshot_film(data_kp),
            'actors': actors_film(kp),
            'trailer': trailer_film(kp),
        }
        return result
    # raise Http404
    else:
        raise Http404
