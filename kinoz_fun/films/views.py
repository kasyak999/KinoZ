from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
# Http404
import requests
from pprint import pprint
from . import key_name  # Импорт переменых и токенов для подключения к Api
from films.models import FilmsdModel
import sqlite3
from django.utils import timezone
import json


def add_scrinshot_film(data_kp):
    """Добавление кадров из фильма с кинопоиска"""
    data_kp += '/images'
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
    if response_kp.status_code == 200:
        scrinshot = response_kp.json()['items']
        # pprint(scrinshot)
        return scrinshot


def information_film(kp):
    """Собираем информацию о фильме из кинопоиска"""
    data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN + str(kp)
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
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

        votecount = f"{response_kp['ratingKinopoiskVoteCount']:,}".replace(',', ' ')
        genres = [list(dict.values(i))[0] for i in response_kp['genres']]
        genres = ', '.join(genres)
        country = [list(dict.values(i))[0] for i in response_kp['countries']]
        country = ', '.join(country)

        result = {
            'id_kp': response_kp['kinopoiskId'],
            'name': response_kp['nameRu'],
            'name_orig': response_kp['nameOriginal'],
            'year': response_kp['year'],
            'poster': (response_kp['posterUrl'], response_kp['posterUrlPreview']),
            'country': country,
            'genres': genres,
            'rating': response_kp['ratingKinopoisk'],
            'votecount': votecount,
            'description': response_kp['description'],
            'cat': cat,
            'scrinshot': scrinshot,
        }
        return result
    raise Http404


def select_database(kp):
    """Вывод из базы данных"""
    result_sql = get_object_or_404(
        FilmsdModel.objects.filter(
            is_published=True, id_kp=kp
        ).select_related('cat'),
        id_kp=kp
    )
    # print(result_sql.name)
    genres = [genre.name for genre in result_sql.genres.values('name')]
    genres = ', '.join(genres)
    country = [country for country in result_sql.country.values('name')]
    # доделать тут
    country = ', '.join(country[0].value())
    print(country)
    if 'url' in result_sql.poster:
        poster = (result_sql.poster['url'], result_sql.poster['prev'])
    else:
        poster = result_sql.poster
    result = {
            'name': result_sql.name,
            'name_orig': result_sql.name_orig,
            'year': result_sql.year,
            'poster': poster,
            'country': country,
            'genres': genres,
            'rating': result_sql.rating,
            'votecount': result_sql.votecount,
            'description': result_sql.description,
            'cat': result_sql.cat['name'],
            'scrinshot': result_sql.scrinshot,
        }
    return result


def add_bd_sql(result):
    """Добавление в базу данных"""
    # json_string = json.dumps(dict())
    # print(json_string)

    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_SELECT = '''
        SELECT MAX(id)
        FROM films_filmsdmodel;
    '''
    sql_INSERT = '''
        INSERT INTO films_filmsdmodel
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    id_add = cur.execute(sql_SELECT)
    id_add = id_add.fetchone()
    id_add = id_add[0] + 1 if id_add[0] is not None else 1
    sql_request = (
        id_add, timezone.now(), 0,
        result['id_kp'], 'Название', None,
        '2024', json.dumps(dict()), None,
        None, 'Нет', 0,
        json.dumps(list()),
    )
    cur.execute(sql_INSERT, sql_request)
    con.commit()
    con.close()


def film(request: HttpRequest, kp: int) -> HttpResponse:
    """ страница фильма """
    # -----------------------------
    result_sql = FilmsdModel.objects.filter(
        id_kp=kp
    ).values('id_kp')
    if result_sql:  # Есть в базе
        result = select_database(kp)
    else:
        print('нет в базе')
        # data = {
        #     'kinopoisk_id': kp,
        #     'api_token': key_name.TOKEN,
        # }
        # response = requests.get(key_name.API_URL, data)
        # if response.json()['result']:
        #     result = response.json()['data'][0]
        # else:
        #     raise Http404
        # # блок с фреймом видео

        result = information_film(kp)
        add_bd_sql(result)

    return render(
        request, 'films/film.html', {'result_kp': result}
    )
    # print('ошибка')
    # raise Http404
