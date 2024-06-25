from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
# Http404
from films.models import FilmsdModel
import json


def index(request: HttpRequest) -> HttpResponse:
    """ Главная страница """
    # result_sql = FilmsdModel.objects.filter(
    #     is_published=True).select_related('cat')
    # # pprint(result_sql)
    # poster = result_sql.poster.split(', ')
    # votecount = f"{result_sql.votecount:,}".replace(',', ' ')
    # scrinshot = json.loads(result_sql.scrinshot)
    # result = {
    #         'name': result_sql.name,
    #         'name_orig': result_sql.name_orig,
    #         'year': result_sql.year,
    #         'poster': poster,
    #         'rating': result_sql.rating,
    #         'votecount': votecount,
    #         'description': result_sql.description,
    #         'cat': result_sql.cat,
    #         'scrinshot': scrinshot,
    #     }
    context = {
        'html_title': 'Гланвая страница',
        'html_name': 'Главная',
        'results': [i for i in range(666, 670)],
    }
    return render(request, 'index/index.html', context)


def contacts(request: HttpRequest) -> HttpResponse:
    """Страница контакты"""
    context = {
        'title': 'Контакты',
    }
    return render(request, 'index/contacts.html', context)
