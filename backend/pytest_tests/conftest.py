import pytest
from django.test.client import Client
from films.models import FilmsdModel, Coment


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
def films_baza():
    return FilmsdModel.objects.create(
        is_published=True,
        verified=True,
        id_kp=1,
        name_orig='Оригинальное название',
        year=2024,
    )


@pytest.fixture
def comments_add(films_baza, author):
    return Coment.objects.create(
        text='Какой то текст',
        film=films_baza,
        author=author,
    )
