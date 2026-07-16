"""Tests unitarios del caso de uso ListPostsUseCase."""
import pytest

from app.application.list_posts import ListPostsUseCase


@pytest.fixture
def use_case(repo):
    """El caso de uso con el fake ya inyectado."""
    return ListPostsUseCase(repo)


def test_sin_posts_devuelve_lista_vacia(use_case):
    """Un blog vacío no es un error."""
    assert use_case.execute() == []


def test_devuelve_los_posts_publicados(use_case, make_publicado):
    a = make_publicado(title="Post A")
    b = make_publicado(title="Post B")
    assert use_case.execute() == [a, b]


def test_no_devuelve_borradores(use_case, repo, make_post, make_publicado):
    """Los borradores NO son visibles en el blog público."""
    publicado = make_publicado(title="Publicado")
    borrador = repo.guardar(make_post(title="Borrador"))

    resultado = use_case.execute()

    assert resultado == [publicado]
    assert borrador not in resultado
