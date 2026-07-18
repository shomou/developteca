"""Tests unitarios del caso de uso AuthenticateUserUseCase."""
import pytest

from app.application.authenticate_user import (
    AuthenticateUserCommand,
    AuthenticateUserUseCase,
)
from app.domain.exceptions import InvalidCredentialsError


@pytest.fixture
def use_case(user_repo, hasher):
    """El caso de uso con los DOS fakes ya inyectados."""
    return AuthenticateUserUseCase(user_repo, hasher)


def test_login_correcto_devuelve_al_usuario(use_case, user_repo, make_user):
    guardado = user_repo.guardar(
        make_user(email_str="ana@developteca.com", password="secreta123")
    )

    resultado = use_case.execute(
        AuthenticateUserCommand(email="ana@developteca.com", password="secreta123")
    )

    assert resultado == guardado


def test_password_incorrecta_lanza_error(use_case, user_repo, make_user):
    user_repo.guardar(make_user(password="secreta123"))
    with pytest.raises(InvalidCredentialsError):
        use_case.execute(
            AuthenticateUserCommand(email="admin@developteca.com", password="mala")
        )


def test_email_inexistente_lanza_el_mismo_error(use_case):
    """Mismo error que password mala: no revelamos si el email existe."""
    with pytest.raises(InvalidCredentialsError):
        use_case.execute(
            AuthenticateUserCommand(email="fantasma@ejemplo.com", password="lo-que-sea")
        )


def test_ambos_fallos_dan_el_mismo_mensaje(use_case, user_repo, make_user):
    """Anti user-enumeration: los dos caminos son indistinguibles."""
    user_repo.guardar(make_user(password="secreta123"))

    with pytest.raises(InvalidCredentialsError) as err_password:
        use_case.execute(
            AuthenticateUserCommand(email="admin@developteca.com", password="mala")
        )
    with pytest.raises(InvalidCredentialsError) as err_email:
        use_case.execute(
            AuthenticateUserCommand(email="nadie@ejemplo.com", password="mala")
        )

    assert str(err_password.value) == str(err_email.value)
