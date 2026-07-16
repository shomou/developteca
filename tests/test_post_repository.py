"""Tests del puerto PostRepository usando un fake en memoria."""
import pytest

from app.domain.ports import PostRepository
from tests.fakes import InMemoryPostRepository


def test_no_se_puede_instanciar_el_puerto():
    """PostRepository es abstracto: es un contrato, no una implementación."""
    with pytest.raises(TypeError):
        PostRepository()


def test_el_fake_cumple_el_contrato():
    """El fake ES un PostRepository a ojos del dominio."""
    assert isinstance(InMemoryPostRepository(), PostRepository)


def test_guardar_asigna_id(repo, make_post):
    post = repo.guardar(make_post())
    assert post.id == 1


def test_buscar_por_id_devuelve_el_post(repo, make_post):
    guardado = repo.guardar(make_post())
    assert repo.buscar_por_id(guardado.id) == guardado


def test_buscar_por_id_inexistente_devuelve_none(repo):
    assert repo.buscar_por_id(999) is None


def test_listar_publicados_solo_devuelve_publicados(repo, make_post, make_publicado):
    borrador = repo.guardar(make_post(title="Borrador"))
    publicado = make_publicado(title="Publicado")

    resultado = repo.listar_publicados()

    assert resultado == [publicado]
    assert borrador not in resultado


def test_eliminar_quita_el_post(repo, make_post):
    post = repo.guardar(make_post())
    repo.eliminar(post.id)
    assert repo.buscar_por_id(post.id) is None
