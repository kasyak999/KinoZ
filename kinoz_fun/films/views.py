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


def information_film(kp: int):
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
            'poster': (response_kp['posterUrl'], response_kp['posterUrlPreview']),
            'country': country,
            'genres': genres,
            'rating': response_kp['ratingKinopoisk'],
            'votecount': response_kp['ratingKinopoiskVoteCount'],
            'description': response_kp['description'],
            'cat': cat,
            'scrinshot': scrinshot,
        }
        return result
    raise Http404


def select_database(kp: int):
    """Вывод из базы данных"""
    result_sql = get_object_or_404(
        FilmsdModel.objects.select_related('cat').prefetch_related(
            'genres', 'country'
        ),
        id_kp=kp, is_published=True
    )
    scrinshot = (
        json.loads(result_sql.scrinshot)
        if result_sql.scrinshot
        else result_sql.scrinshot
    )
    result = {
            'name': result_sql.name,
            'name_orig': result_sql.name_orig,
            'year': result_sql.year,
            'poster': result_sql.poster,
            'country': result_sql.country,
            'genres': result_sql.genres,
            'rating': result_sql.rating,
            'votecount': result_sql.votecount,
            'description': result_sql.description,
            'cat': result_sql.cat,
            'scrinshot': scrinshot,
        }
    return result


def add_bd_sql(result):
    """Добавление в базу данных"""
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    sql_select = '''
        SELECT MAX(id)
        FROM films_filmsdmodel;
    '''
    sql_inzert = '''
        INSERT INTO films_filmsdmodel
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    poster = ', '.join(result['poster'])
    scrinshot = json.dumps(result['scrinshot'])
    id_add = cur.execute(sql_select)
    id_add = id_add.fetchone()
    id_add = id_add[0] + 1 if id_add[0] is not None else 1
    sql_request = (
        id_add, timezone.now(), result['name'],
        1, result['id_kp'], result['name_orig'], result['year'],
        poster, result['rating'], result['votecount'],
        result['description'], None, scrinshot,
    )
    cur.execute(sql_inzert, sql_request)
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
        print('есть')
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

        add_bd_sql(information_film(kp))
        result = select_database(kp)

    return render(
        request, 'films/film.html', {'result': result}
    )
    # print('ошибка')
    # raise Http404
