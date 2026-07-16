"""Tests unitarios de la entidad Post."""
import pytest

from app.domain.entities import PostStatus
from app.domain.exceptions import InvalidPostError, PostAlreadyPublishedError


def test_post_nuevo_nace_como_borrador(make_post):
    post = make_post()
    assert post.status is PostStatus.DRAFT
    assert post.esta_publicado is False
    assert post.published_at is None


def test_titulo_vacio_lanza_error(make_post):
    with pytest.raises(InvalidPostError):
        make_post(title="   ")


def test_publicar_cambia_estado_y_registra_fecha(make_post):
    post = make_post()
    post.publicar()
    assert post.esta_publicado is True
    assert post.status is PostStatus.PUBLISHED
    assert post.published_at is not None


def test_no_se_puede_publicar_dos_veces(make_post):
    post = make_post()
    post.publicar()
    with pytest.raises(PostAlreadyPublishedError):
        post.publicar()


def test_no_se_puede_publicar_sin_contenido(make_post):
    post = make_post(content="")
    with pytest.raises(InvalidPostError):
        post.publicar()
    assert post.esta_publicado is False


def test_identidad_mismo_id_son_el_mismo_post(make_post):
    """Aunque cambie el título, el id manda."""
    assert make_post(id=1, title="Titulo A") == make_post(id=1, title="Titulo B")


def test_posts_sin_id_no_son_iguales(make_post):
    assert make_post() != make_post()
