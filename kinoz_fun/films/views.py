from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpRequest, Http404
# Http404
import requests
from pprint import pprint
from . import key_name  # Импорт переменых и токенов для подключения к Api
from films.models import FilmsdModel, Category


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


def select_database(result_sql):
    """Вывод из базы данных"""
    genres = [genre.name for genre in result_sql[0].genres.all()]
    genres = ', '.join(genres)
    country = [country.name for country in result_sql[0].country.all()]
    country = ', '.join(country)
    if 'url' in result_sql[0].poster:
        poster = (result_sql[0].poster['url'], result_sql[0].poster['prev'])
    else:
        poster = result_sql[0].poster
    result = {
            'name': result_sql[0].name,
            'name_orig': result_sql[0].name_orig,
            'year': result_sql[0].year,
            'poster': poster,
            'country': country,
            'genres': genres,
            'rating': result_sql[0].rating,
            'votecount': result_sql[0].votecount,
            'description': result_sql[0].description,
            'cat': result_sql[0].cat.name,
            'scrinshot': result_sql[0].scrinshot,
        }
    return result


def film(request: HttpRequest, kp: int) -> HttpResponse:
    """ страница фильма """
    # -----------------------------
    result_sql = FilmsdModel.objects.filter(
        is_published=True,
        id_kp=kp
    ).select_related('cat')
    if result_sql:  # Есть в базе
        result = select_database(result_sql)
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
    return render(
        request, 'films/film.html', {'result_kp': result}
    )
    # print('ошибка')
    # raise Http404
