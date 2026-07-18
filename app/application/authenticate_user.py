"""
Caso de uso: autenticar a un usuario (login)

Orquesta DOS puertos: busca al usuario por email (UserRepository) y verifica
su contraseña (PasswordHasher). Solo si ambas cosas son correctas, autentica.
"""
from dataclasses import dataclass

from app.domain.entities import User
from app.domain.exceptions import InvalidCredentialsError
from app.domain.ports import PasswordHasher, UserRepository

@dataclass(frozen=True)
class AuthenticateUserCommand:
    """Credenciales de entrada login."""
    
    email: str
    password: str

class AuthenticateUserUseCase:
    """Verifica las credenciales de un usuario."""
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ) -> None:
        """Recibe dos puertos por inyección de dependencias.
        
        Args:
            user_repository: para localizar al usuario por su email.
            password_hasher: para verificar la contraseña contra el hash.
        """
        self._users = user_repository
        self._hasher = password_hasher
        
    def execute(self, command: AuthenticateUserCommand) -> User:
        """Ejecuta el login.
        
        Args:
            command: email y contraseña en texto plano.
            
        Returns:
            User: el usuario autenticado
        
        Reises:
            InvalidCredentialsError: si el email no existe o la contraseña es
                incorrecta. Deliberadamente NO se distingue entre ambos casos.
        """
        user = self._users.buscar_por_email(command.email)
        
        # Mismo error tanto si el usuario no existe como si la clave falla.
        if user is None:
            raise InvalidCredentialsError("Email o contraseña incorrectos.")
        
        if not self._hasher.verify(command.password, user.password_hash):
            raise InvalidCredentialsError("Email o contraseña incorrectos.")
        
        return user