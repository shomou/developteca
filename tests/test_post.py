"""Tests unitarios de la entidad Post."""
import pytest

from app.domain.entities import Post, PostStatus
from app.domain.exceptions import InvalidPostError, PostAlreadyPublishedError


def _post(**overrides):
    """Helper: crea un Post válido; permite sobreescribir campos."""
    datos = {
        "title": "Mi primer post",
        "content": "Contenido en **Markdown**",
        "author_id": 1,
    }
    datos.update(overrides)
    return Post(**datos)


def test_post_nuevo_nace_como_borrador():
    post = _post()
    assert post.status is PostStatus.DRAFT
    assert post.esta_publicado is False
    assert post.published_at is None


def test_titulo_vacio_lanza_error():
    with pytest.raises(InvalidPostError):
        _post(title="   ")


def test_publicar_cambia_estado_y_registra_fecha():
    post = _post()
    post.publicar()
    assert post.esta_publicado is True
    assert post.status is PostStatus.PUBLISHED
    assert post.published_at is not None


def test_no_se_puede_publicar_dos_veces():
    post = _post()
    post.publicar()
    with pytest.raises(PostAlreadyPublishedError):
        post.publicar()


def test_no_se_puede_publicar_sin_contenido():
    post = _post(content="")
    with pytest.raises(InvalidPostError):
        post.publicar()
    assert post.esta_publicado is False  # sigue en borrador


def test_identidad_mismo_id_son_el_mismo_post():
    """Aunque cambie el título, el id manda."""
    assert _post(id=1, title="Titulo A") == _post(id=1, title="Titulo B")


def test_posts_sin_id_no_son_iguales():
    """Dos posts nuevos distintos, aunque tengan los mismos datos."""
    assert _post() != _post()