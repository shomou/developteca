"""Tests unitarios del caso de uso UpdatePostUseCase."""
import pytest

from app.application.update_post import UpdatePostCommand, UpdatePostUseCase
from app.domain.exceptions import InvalidPostError, PostNotFoundError


@pytest.fixture
def use_case(repo):
    """El caso de uso con el fake ya inyectado."""
    return UpdatePostUseCase(repo)


def test_actualiza_el_post(use_case, repo, make_post):
    post = repo.guardar(make_post())

    resultado = use_case.execute(
        UpdatePostCommand(post_id=post.id, title="Nuevo", content="Texto nuevo")
    )

    assert resultado.title == "Nuevo"
    assert resultado.content == "Texto nuevo"


def test_el_cambio_queda_persistido(use_case, repo, make_post):
    post = repo.guardar(make_post())

    use_case.execute(
        UpdatePostCommand(post_id=post.id, title="Nuevo", content="Texto nuevo")
    )

    assert repo.buscar_por_id(post.id).title == "Nuevo"


def test_post_inexistente_lanza_error(use_case):
    with pytest.raises(PostNotFoundError):
        use_case.execute(UpdatePostCommand(post_id=999, title="X", content="Y"))


def test_titulo_invalido_lanza_error(use_case, repo, make_post):
    post = repo.guardar(make_post())
    with pytest.raises(InvalidPostError):
        use_case.execute(
            UpdatePostCommand(post_id=post.id, title="", content="Texto")
        )


def test_se_puede_editar_un_post_publicado(use_case, make_publicado):
    """Corregir una errata no despublica el post."""
    post = make_publicado()

    resultado = use_case.execute(
        UpdatePostCommand(post_id=post.id, title="Corregido", content="Texto")
    )

    assert resultado.title == "Corregido"
    assert resultado.esta_publicado is True
