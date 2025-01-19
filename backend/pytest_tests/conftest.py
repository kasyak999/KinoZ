import pytest
from django.test.client import Client
from films.models import FilmsdModel, Coment, Favorite
from users.models import Follow, Message


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Avtar')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Notavtar')


@pytest.fixture
def author_client(author):
    """Авторизированный автор"""
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    """Авторизированый не автор"""
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def films_true():
    return FilmsdModel.objects.create(
        is_published=True,
        verified=True,
        id_kp=1,
        name='Оригинальное название',
        year=2024,
    )


@pytest.fixture
def is_published_false():
    return FilmsdModel.objects.create(
        is_published=False,
        verified=True,
        id_kp=2,
        name='Оригинальное название2',
        year=2024,
    )


@pytest.fixture
def verified_false():
    return FilmsdModel.objects.create(
        is_published=True,
        verified=False,
        id_kp=3,
        name='Оригинальное название3',
        year=2024,
    )


@pytest.fixture
def films_false():
    return FilmsdModel.objects.create(
        is_published=False,
        verified=False,
        id_kp=4,
        name='Оригинальное название4',
        year=2024,
    )


@pytest.fixture
def comments_add(films_true, author):
    return Coment.objects.create(
        text='Какой то текст',
        film=films_true,
        author=author,
    )


@pytest.fixture
def favorite(films_true, author):
    return Favorite.objects.create(
        user=author,
        film=films_true,
    )


@pytest.fixture
def follow(author, not_author):
    return Follow.objects.create(
        user=author,
        following=not_author,
    )


@pytest.fixture
def message(author, not_author):
    return Message.objects.create(
        sender=author,
        receiver=not_author,
        content='Текст',
    )
