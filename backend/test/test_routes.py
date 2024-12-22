from http import HTTPStatus
import pytest
from django.urls import reverse
from films.models import FilmsdModel


@pytest.fixture
def urls(films_baza):
    """Фикстура для url"""
    return {
        'index': reverse('films:index'),
        'film': reverse('films:film', args=[films_baza.id_kp]),
    }


@pytest.mark.parametrize(
    'name_url',
    (
        'index',
        'film'
    )
)
@pytest.mark.parametrize(
    'client_, code',
    (
        ('author_client', HTTPStatus.OK),
        ('not_author_client', HTTPStatus.OK),
        ('client', HTTPStatus.OK),
    )
)
@pytest.mark.django_db
def test_status_codes(name_url, code, films_baza, urls, client_, request):
    """Проверка статуса страниц"""
    count = FilmsdModel.objects.count()
    client_ = request.getfixturevalue(client_)
    assert client_.get(urls[name_url]), code
    assert FilmsdModel.objects.count() == count
