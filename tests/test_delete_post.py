"""Tests unitarios del caso de uso DeletePostUseCase."""
import pytest

from app.application.delete_post import DeletePostUseCase
from app.domain.exceptions import PostNotFoundError


@pytest.fixture
def use_case(repo):
    """El caso de uso con el fake ya inyectado."""
    return DeletePostUseCase(repo)


def test_elimina_el_post(use_case, repo, make_post):
    post = repo.guardar(make_post())
    use_case.execute(post.id)
    assert repo.buscar_por_id(post.id) is None


def test_post_inexistente_lanza_error(use_case):
    """Borrar algo que no existe debe avisar, no fingir éxito."""
    with pytest.raises(PostNotFoundError):
        use_case.execute(999)


def test_solo_elimina_el_indicado(use_case, repo, make_post):
    """No debe llevarse por delante otros posts."""
    a = repo.guardar(make_post(title="A"))
    b = repo.guardar(make_post(title="B"))

    use_case.execute(a.id)

    assert repo.buscar_por_id(a.id) is None
    assert repo.buscar_por_id(b.id) == b
