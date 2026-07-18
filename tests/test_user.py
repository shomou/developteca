"""Tests unitarios de la entidad User y del puerto PasswordHasher."""
import pytest

from app.domain.entities import User
from app.domain.exceptions import InvalidUserError
from app.domain.ports import PasswordHasher, UserRepository
from app.domain.value_objects import Email
from tests.fakes import FakePasswordHasher, InMemoryUserRepository

def test_user_valido_se_crea(make_user):
    user =  make_user()
    assert user.username == "admin"
    assert user.email.value == "admin@developteca.com"

def test_username_vacio_lanza_error(make_user):
    with pytest.raises(InvalidUserError):
        make_user(username="   ")
        
def test_email_debe_ser_value_object(make_user):
    """Un str no basta: el tipo Email garantiza que ya está validado."""
    with pytest.raises(InvalidUserError):
        make_user(email="admin@developteca.com")

def test_no_se_guarda_la_password_en_claro(make_user, hasher):
    """La entidad guarda el hash, no la contraseña tal como la tecleó el usuario."""
    user = make_user(password="secreta123")
    # No almacena el texto plano crudo; almacena el resultado de hashear.
    assert user.password_hash != "secreta123"
    assert user.password_hash == hasher.hash("secreta123")


def test_identidad_por_id(make_user):
    assert make_user(id=1, username="ana") == make_user(id=1, username="luis")


# --- Puertos ---

def test_los_puertos_son_abstractos():
    with pytest.raises(TypeError):
        UserRepository()
    with pytest.raises(TypeError):
        PasswordHasher()


def test_los_fakes_cumplen_los_contratos():
    assert isinstance(InMemoryUserRepository(), UserRepository)
    assert isinstance(FakePasswordHasher(), PasswordHasher)


def test_hasher_verifica_password_correcta(hasher):
    h = hasher.hash("secreta123")
    assert hasher.verify("secreta123", h) is True


def test_hasher_rechaza_password_incorrecta(hasher):
    h = hasher.hash("secreta123")
    assert hasher.verify("otra-cosa", h) is False


# --- Repositorio ---

def test_buscar_por_email_encuentra_al_usuario(user_repo, make_user):
    user = user_repo.guardar(make_user())
    assert user_repo.buscar_por_email("admin@developteca.com") == user


def test_buscar_por_email_inexistente_devuelve_none(user_repo):
    assert user_repo.buscar_por_email("nadie@ejemplo.com") is None