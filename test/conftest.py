import pytest
from django.test.client import Client
from films.models import FilmsdModel


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def films_baza():
    return FilmsdModel.objects.create(
        is_published=True,
        id_kp=1,
        name_orig='Оригинальное название',
        year=2024,
    )
