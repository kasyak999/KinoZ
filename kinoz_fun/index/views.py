from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, HttpRequest
# Http404
from films.models import FilmsdModel
from pprint import pprint
from django.utils import timezone
import sqlite3
import key_name  # Импорт переменых и токенов для подключения к Api
import requests


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница """
    # get_object_or_404
    results = get_list_or_404(FilmsdModel.objects.select_related(
        'cat').prefetch_related(
            'genres', 'country'
        ), is_published=True
    )
    context = {
        'html_title': 'Гланвая страница',
        'html_name': 'Главная',
        'results': results,
        # 'results': [i for i in range(666, 670)],
    }
    return render(request, 'index/index.html', context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Страница контакты"""
    context = {
        'title': 'Контакты',
    }
    return render(request, 'index/contacts.html', context)


def add_country(request: HttpRequest) -> HttpResponse:
    """ Добавление стран фильмов в базу"""
    data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN
    data_kp += '/filters'
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
    if response_kp.status_code == 200:
        results = response_kp.json()['countries']
        print(results)
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        for i in results:
            print(i['country'])
            sql_select = '''
                SELECT MAX(id)
                FROM films_country;
            '''
            id_add = cur.execute(sql_select)
            id_add = id_add.fetchone()
            id_add = id_add[0] + 1 if id_add[0] is not None else 1
            print(id_add)
            sql_inzert = '''
                INSERT INTO films_country
                VALUES(?, ?, ?);
            '''
            sql_request = (
                id_add, timezone.now(), i['country']
            )
            cur.execute(sql_inzert, sql_request)
            con.commit()
            # con.close()
    return render(request, 'index/index.html')


def add_genres(request: HttpRequest) -> HttpResponse:
    """ Добавление жанров фильмов в базу"""
    data_kp = key_name.KINOPOISK_URL + key_name.KINOPOISK_URL_MAIN
    data_kp += '/filters'
    response_kp = requests.get(data_kp, headers=key_name.DATA_KP)
    if response_kp.status_code == 200:
        results = response_kp.json()['genres']
        # print(results)
        con = sqlite3.connect('db.sqlite3')
        cur = con.cursor()
        for i in results:
            print(i['genre'])
            sql_select = '''
                SELECT MAX(id)
                FROM films_genres;
            '''
            id_add = cur.execute(sql_select)
            id_add = id_add.fetchone()
            id_add = id_add[0] + 1 if id_add[0] is not None else 1
            print(id_add)
            sql_inzert = '''
                INSERT INTO films_genres
                VALUES(?, ?, ?);
            '''
            sql_request = (
                id_add, timezone.now(), i['genre']
            )
            cur.execute(sql_inzert, sql_request)
            con.commit()
            # con.close()
    return render(request, 'index/index.html')
