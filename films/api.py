from django.http import Http404
# Http404
import requests
import films.key_name as key_name  # Импорт переменых и токенов для подключения к Api
import sqlite3
import json
from django.utils import timezone


def add_scrinshot_film(data_kp):
    """Добавление кадров из фильма с кинопоиска"""
    data_kp += '/images'
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
    if response_kp.status_code == 200:
        scrinshot = response_kp.json()['items']
        # print('--------------------------------------')
        # print(scrinshot)
        print('--------------------------------------')
        return scrinshot


def information_film(kp: int):
    """Собираем информацию о фильме из кинопоиска"""
    data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN + str(kp)
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
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
            'poster': f"{response_kp['posterUrl']}, {response_kp['posterUrlPreview']}",
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
        return False
