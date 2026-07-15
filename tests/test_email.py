"""Tests unitarios del Value Object Email."""
import pytest

from app.domain.value_objects import Email
from app.domain.exceptions import InvalidEmailError


def test_email_valido_se_crea():
    """Un email con formato correcto se crea sin errores."""
    email = Email("juan@ejemplo.com")
    assert email.value == "juan@ejemplo.com"


def test_dos_emails_iguales_por_valor():
    """Igualdad por valor: mismo texto => mismo Email."""
    assert Email("a@b.com") == Email("a@b.com")


def test_email_es_inmutable():
    """No se puede modificar tras crearlo (frozen)."""
    email = Email("a@b.com")
    with pytest.raises(Exception):
        email.value = "otro@b.com"


@pytest.mark.parametrize("invalido", ["sin-arroba", "@sindominio", "a@b", "a b@c.com", ""])
def test_email_invalido_lanza_error(invalido):
    """Formatos inválidos lanzan InvalidEmailError."""
    with pytest.raises(InvalidEmailError):
        Email(invalido)