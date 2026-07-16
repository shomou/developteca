"""
Fixtures compartidas por todos los tests.

pytest descubre este archivo automáticamente: las fixtures definidas aquí
están disponibles en cualquier test SIN necesidad de importarlas.
"""
import pytest

from app.domain.entities import Post
from tests.fakes import InMemoryPostRepository


@pytest.fixture
def repo():
    """Repositorio en memoria, limpio para cada test."""
    return InMemoryPostRepository()


@pytest.fixture
def make_post():
    """Factory de Posts válidos (en borrador).

    Devuelve una FUNCIÓN, no un Post: así cada test crea los que necesite
    y personaliza solo los campos que le importan.

    Uso:
        def test_algo(make_post):
            post = make_post(title="Otro título")
    """

    def _make(**overrides):
        datos = {
            "title": "Hola mundo",
            "content": "Contenido en **Markdown**",
            "author_id": 1,
        }
        datos.update(overrides)
        return Post(**datos)

    return _make


@pytest.fixture
def make_publicado(repo, make_post):
    """Factory de posts YA publicados y guardados en el repo.

    Nota: una fixture puede usar otras fixtures (aquí, repo y make_post).
    """

    def _make(**overrides):
        post = make_post(**overrides)
        post.publicar()
        return repo.guardar(post)

    return _make
