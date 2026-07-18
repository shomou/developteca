"""
Fixtures compartidas por todos los tests.

pytest descubre este archivo automáticamente: las fixtures definidas aquí
están disponibles en cualquier test SIN necesidad de importarlas.
"""
import pytest

from app.domain.entities import Post, User
from app.domain.value_objects import Email
from tests.fakes import InMemoryPostRepository,  InMemoryUserRepository, FakePasswordHasher


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

@pytest.fixture
def user_repo():
    """Repositorio de usuarios en memoria, limpio para cada test."""
    return InMemoryUserRepository()

@pytest.fixture
def hasher():
    """Hasher false (rapido) para tests."""
    return FakePasswordHasher()

@pytest.fixture
def make_user(hasher):
    """Factory de Users válidos.

    Recibe la contraseña en texto plano (la hashea con el fake hasher) y,
    opcionalmente, el email como string vía email_str.
    """

    def _make(password="secreta123", email_str="admin@developteca.com", **overrides):
        datos = {
            "username": "admin",
            "email": Email(email_str),
            "password_hash": hasher.hash(password),
        }
        datos.update(overrides)
        return User(**datos)

    return _make