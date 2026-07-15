"""Tests unitarios del caso de uso CreatePostUseCase."""
import pytest

from app.application.create_post import CreatePostCommand, CreatePostUseCase
from app.domain.entities import PostStatus
from app.domain.exceptions import InvalidPostError
from tests.fakes import InMemoryPostRepository


@pytest.fixture
def repo():
    """Repositorio en memoria, limpio para cada test."""
    return InMemoryPostRepository()


@pytest.fixture
def use_case(repo):
    """El caso de uso con el fake YA INYECTADO."""
    return CreatePostUseCase(repo)


def _comando(**overrides):
    """Helper: un comando válido; permite sobreescribir campos."""
    datos = {"title": "Hola mundo", "content": "Contenido en **Markdown**", "author_id": 1}
    datos.update(overrides)
    return CreatePostCommand(**datos)


def test_crea_el_post_y_le_asigna_id(use_case):
    post = use_case.execute(_comando())
    assert post.id == 1
    assert post.title == "Hola mundo"


def test_el_post_creado_nace_como_borrador(use_case):
    """Crear != publicar: nace en DRAFT."""
    post = use_case.execute(_comando())
    assert post.status is PostStatus.DRAFT


def test_el_post_queda_guardado_en_el_repositorio(use_case, repo):
    """Verifica el efecto secundario: realmente se persistió."""
    post = use_case.execute(_comando())
    assert repo.buscar_por_id(post.id) == post


def test_titulo_invalido_propaga_error_del_dominio(use_case):
    """La regla vive en la entidad; el caso de uso deja pasar el error."""
    with pytest.raises(InvalidPostError):
        use_case.execute(_comando(title=""))


def test_titulo_invalido_no_guarda_nada(use_case, repo):
    """Si la entidad se rechaza, nunca se llama a guardar."""
    with pytest.raises(InvalidPostError):
        use_case.execute(_comando(title=""))
    assert repo.buscar_por_id(1) is None
