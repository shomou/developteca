"""Tests unitarios del caso de uso PublishPostUseCase."""
import pytest

from app.application.publish_post import PublishPostUseCase
from app.domain.entities import PostStatus
from app.domain.exceptions import (
    InvalidPostError,
    PostAlreadyPublishedError,
    PostNotFoundError,
)


@pytest.fixture
def use_case(repo):
    """El caso de uso con el fake ya inyectado."""
    return PublishPostUseCase(repo)


def test_publica_el_post(use_case, repo, make_post):
    post = repo.guardar(make_post())
    resultado = use_case.execute(post.id)
    assert resultado.status is PostStatus.PUBLISHED
    assert resultado.published_at is not None


def test_el_cambio_queda_persistido(use_case, repo, make_post):
    post = repo.guardar(make_post())
    use_case.execute(post.id)
    assert repo.buscar_por_id(post.id).esta_publicado is True


def test_aparece_en_listar_publicados(use_case, repo, make_post):
    post = repo.guardar(make_post())
    use_case.execute(post.id)
    assert repo.listar_publicados() == [post]


def test_post_inexistente_lanza_error(use_case):
    with pytest.raises(PostNotFoundError):
        use_case.execute(999)


def test_publicar_dos_veces_lanza_error(use_case, repo, make_post):
    post = repo.guardar(make_post())
    use_case.execute(post.id)
    with pytest.raises(PostAlreadyPublishedError):
        use_case.execute(post.id)


def test_post_sin_contenido_no_se_publica(use_case, repo, make_post):
    post = repo.guardar(make_post(content=""))
    with pytest.raises(InvalidPostError):
        use_case.execute(post.id)
    assert repo.buscar_por_id(post.id).esta_publicado is False
