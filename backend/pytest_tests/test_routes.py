import pytest
from http import HTTPStatus
from pytest_django.asserts import assertRedirects
from django.urls import reverse


@pytest.fixture
def urls(films_baza, author, comments_add):
    """Фикстура для url"""
    return {
        'index': reverse('films:index'),
        'film': reverse('films:film', args=[films_baza.id_kp]),
        'search': reverse('films:search'),
        'add_film': reverse('films:add_film'),
        'user_list': reverse('users:user_list'),
        'registration': reverse('users:registration'),

        'user': reverse('users:user', args=[author.username]),
        'edit_account': reverse(
            'users:edit_account', args=[author.username]),
        'user_following': reverse(
            'users:user_following', args=[author.username]),
        'user_followers': reverse(
            'users:user_followers', args=[author.username]),
        'message_list': reverse('users:message_list'),
        'message_username': reverse(
            'users:message_username', args=[author.username]),

        'edit_comment': reverse(
            'films:edit_comment', kwargs={
                'film_id_kp': films_baza.id_kp,
                'comment_id': comments_add.id}
        ),
        'delete_comment': reverse(
            'films:delete_comment', kwargs={
                'film_id_kp': films_baza.id_kp,
                'comment_id': comments_add.id}
        ),
    }


@pytest.mark.parametrize(
    'name_url',
    (
        'index',
        'film',
        'search',
        'add_film',
        'user_list',
        'registration'
    )
)
@pytest.mark.parametrize(
    'client_, code',
    (
        ('author_client', HTTPStatus.OK),
        ('client', HTTPStatus.OK),
    )
)
@pytest.mark.django_db
def test_authorized_and_unauthorized_user_status_codes(
    name_url, code, urls, client_, request
):
    """Проверка доступа общих страниц"""
    client = request.getfixturevalue(client_)
    assert client.get(urls[name_url]).status_code == code


@pytest.mark.parametrize(
    'name_url',
    (
        'user',
        'edit_account',
        'user_following',
        'user_followers',
        'message_list',
        'message_username',
        'edit_comment',
        'delete_comment'
    )
)
@pytest.mark.parametrize(
    'client_, code',
    (
        ('author_client', HTTPStatus.OK),
        ('client', HTTPStatus.FOUND),
    )
)
@pytest.mark.django_db
def test_authorized_and_unauthorized_user_status_codes_2(
    name_url, code, urls, client_, request
):
    """Проверка доступа общих страниц 2"""
    client_autch = request.getfixturevalue(client_)
    if client_ == 'client':
        login_url = reverse('login')
        expected_url = f'{login_url}?next={urls[name_url]}'
        response = client_autch.get(urls[name_url])
        assertRedirects(
            response, expected_url, target_status_code=HTTPStatus.OK)
    assert client_autch.get(urls[name_url]).status_code == code


@pytest.mark.django_db
def test_qwe(client, urls):
    """Проверка редиректа если нет фильма в базе"""
    id_kp = 666
    url = reverse('films:film', args=[id_kp])
    expected_url = f'{urls['add_film']}?id={id_kp}'
    assertRedirects(
        client.get(url), expected_url, status_code=HTTPStatus.FOUND,
        target_status_code=HTTPStatus.OK)
