from pytest_django.asserts import assertRedirects
from django.urls import reverse
from films.models import Coment, Favorite
from users.models import Follow, Message
from news.models import EventUser
import pytest
from http import HTTPStatus


@pytest.fixture
def urls(films_true, comments_add, not_author):
    """Фикстура для url"""
    return {
        'film': reverse('films:film', args=[films_true.id_kp]),
        'edit_comment': reverse('films:edit_comment', args=[
            films_true.id_kp, comments_add.id]),
        'delete_comment': reverse('films:delete_comment', args=[
            films_true.id_kp, comments_add.id]),
        'user': reverse('users:user', args=[not_author.username]),
        'message_username': reverse(
            'users:message_username', args=[not_author.username]),
        'favorite': reverse('films:favorite'),

        'user_following': reverse(
            'users:user_following', args=[not_author.username]),
        'user_followers': reverse(
            'users:user_followers', args=[not_author.username]),
    }


@pytest.fixture
def form_data():
    return {
        'text': 'Новый заголовок',
    }


@pytest.fixture
def form_data1():
    return {
        'content': 'Первое сообщение',
    }


def test_user_create_coment(
        author_client, films_true, form_data, author, urls
):
    """Добавить новый комментарий"""
    count = EventUser.objects.count()
    author_client.post(urls['film'], data={**form_data, 'comment': ''})
    assert Coment.objects.count() == 2, (
        'Комментарии не добавляется к фильму')
    new_coment = Coment.objects.latest('id')
    assert new_coment.text == form_data['text'], (
        'Текст не соответствует отправленому')
    assert new_coment.author == author, (
        'Логин пользователя не соответствует')
    assert new_coment.film == films_true, (
        'Комментарий не соответствует фильму')
    assert EventUser.objects.count() == count + 1


@pytest.mark.parametrize(
    'data_post, url, model, redirects',
    (
        (None, 'delete_comment', Coment, 'film'),
        ({'favorite': ''}, 'film', Favorite, 'film'),
        (None, 'user', Follow, 'user')
    )
)
def test_author_client_delet(
    url, data_post, model, redirects, author_client, urls, favorite, follow
):
    """
    Автор может удалять из избрного фильмы, удалять свои коментарии,
    отписываться от пользователей и добавление новостей его пидписчикам
    """
    count = EventUser.objects.count()
    response = author_client.post(urls[url], data=data_post)
    assertRedirects(response, urls[redirects])
    assert model.objects.count() == 0
    assert EventUser.objects.count() == count + 1


@pytest.mark.parametrize(
    'url, model, rez',
    (
        ('film', Coment, 1),
        ('message_username', Message, 0),
        ('favorite', Favorite, 0),
        ('user_following', Follow, 0),
        ('user_followers', Follow, 0),
    )
)
@pytest.mark.django_db
def test_anonymous_user_create_and_redirect(client, urls, url, model, rez):
    """
    Анонимный пользователь не может выполнять действия предусмотренные
    для авторизированых
    """
    response = client.post(urls[url])
    expected_url = f'{reverse('login')}?next={urls[url]}'
    assertRedirects(
        response, expected_url, msg_prefix='Редирект не соответствует')
    assert model.objects.count() == rez


def test_message_author_client(
    not_author, author, author_client, urls, form_data1
):
    """Автор может отправлять сообщения пользователям"""
    author_client.post(urls['message_username'], form_data1)
    assert Message.objects.count() == 1
    result = Message.objects.get()
    assert result.sender == author
    assert result.receiver == not_author
    assert result.content == form_data1['content']


def test_favorite_author_client_add(author_client, urls, author, films_true):
    """Автор может добавлять фильмы в избраное"""
    count = EventUser.objects.count()
    author_client.post(urls['film'], data={'favorite': ''})
    result = Favorite.objects.get()
    assert result.user == author
    assert result.film == films_true
    assert EventUser.objects.count() == count + 1


def test_coment_not_author_clientt_delete(not_author_client, urls):
    """Не автор не может удалять чужие комментарии"""
    response = not_author_client.post(urls['delete_comment'])
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Coment.objects.count() == 1


def test_coment_not_author_clientt_edit(
    not_author_client, form_data, urls, comments_add
):
    """Не автор не может редактировать чужие комментарии"""
    response = not_author_client.post(urls['edit_comment'], form_data)
    assert response.status_code == HTTPStatus.NOT_FOUND
    coment_from_db = Coment.objects.get(id=comments_add.id)
    assert comments_add.text == coment_from_db.text


def test_coment_author_clientt_edit(
    author_client, form_data, urls, comments_add
):
    """Автор может редактировать свои комментарии"""
    response = author_client.post(urls['edit_comment'], form_data)
    assertRedirects(response, urls['film'])
    comments_add.refresh_from_db()  # Обновляем базу
    assert comments_add.text == form_data['text']


def test_follow_author_client_add(author, author_client, not_author, urls):
    """Автор может подписываться на пользователей"""
    author_client.post(urls['user'])
    assert Follow.objects.count() == 1
    result = Follow.objects.get()
    assert result.following == not_author
    assert result.user == author
