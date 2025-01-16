import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from django.urls import reverse
from pprint import pprint


@pytest.fixture
def urls():
    """Фикстура для url"""
    return {
        'index': reverse('films:index'),
        'favorite': reverse('films:favorite'),
    }


@pytest.mark.parametrize(
    'name_url',
    (
        'index',
        'favorite'
    )
)
@pytest.mark.parametrize(
    'film_status',
    (
        'is_published_false',
        'verified_false',
        'films_false',
    )
)
@pytest.mark.django_db
def test_displaying_movies_on_the_main_page_2(
    film_status, name_url, urls, not_author_client
):
    """Не показывать фильмы на главной которые не проверены"""
    response = not_author_client.get(urls[name_url])
    object_list = response.context['object_list']
    assert film_status not in object_list, (
        'Фильмы, которые не прошли проверку отображатся пользователям')


@pytest.mark.django_db
def test_displaying_movies_on_the_main_page(films_true, urls, client):
    """Отображение фильмов на главной"""
    response = client.get(urls['index'])
    object_list = response.context['object_list']
    assert films_true in object_list, ('Фильмы не отображатся на странице')


@pytest.mark.parametrize(
    'avtar, status',
    (
        ('author_client', True),
        ('not_author_client', False)
    )

)
@pytest.mark.django_db
def test_favorite_films(favorite, urls, avtar, status, request):
    """Проверка избранных фильмов пользователя"""
    client_autch = request.getfixturevalue(avtar)
    response = client_autch.get(urls['favorite'])
    object_list = response.context['object_list']
    assert (favorite.film in object_list) is status, (
        'Фильм отсутствует в избранном списке пользователя'
        ' или присутствует у других')
