import pytest
# from http import HTTPStatus
# from pytest_django.asserts import assertRedirects
from django.urls import reverse
from films.form import ComentForm, FilmLinkForm, FormComment
from users.form import MessageForm


@pytest.fixture
def urls(author, films_true, not_author, comments_add):
    """Фикстура для url"""
    return {
        'index': reverse('films:index'),
        'favorite': reverse('films:favorite'),
        'user': reverse('users:user', args=[author.username]),
        'film': reverse('films:film', args=[films_true.id_kp]),
        'message': reverse('users:message_username', args=[
            not_author.username]),
        'add_film': reverse('films:add_film'),
        'edit_comment': reverse('films:edit_comment', args=[
            films_true.id_kp, comments_add.id]),
        'message_list': reverse('users:message_list'),
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


@pytest.mark.parametrize(
    'url',
    ('film', 'user')
)
@pytest.mark.django_db
def test_user_comments(comments_add, url, urls, author_client, message):
    """Есть ли комментарии пользователя на странице пользователя"""
    response = author_client.get(urls[url])
    object_list = response.context['object_list']
    assert comments_add in object_list, (
        'Отсутствуют комментарии пользователя')


@pytest.mark.django_db
def test_user_message(urls, author_client, message):
    response = author_client.get(urls['message_list'])
    object_list = response.context['object_list']
    assert message in object_list, (
        'Отсутствуют сообщения')


@pytest.mark.parametrize(
    'url, form',
    (
        ('film', ComentForm),
        ('message', MessageForm),
        ('add_film', FilmLinkForm),
        ('edit_comment', FormComment)
    )
)
@pytest.mark.django_db
def test_qwe(films_true, url, form, urls, author_client):
    """Проверка форм"""
    response = author_client.get(urls[url])
    assert 'form' in response.context, f'Нет формы на странице {url}'
    assert isinstance(response.context['form'], form), (
        f'Форма не пренадлежит к классу {form}'
    )
