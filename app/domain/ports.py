"""
Puertos (interfaces) del dominio Developteca.

Un puerto declara QUÉ necesita el dominio del mundo exterior, sin decir CÓMO
se implementa. La infraestructura proveerá los adaptadores concretos.
Aquí NO se menciona SQLAlchemy, PostgreSQL ni Flask: solo el contrato.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Post, User

class PostRepository(ABC):
    """Puerto de salida: contrato de persistencia Posts.
    ABC = Abstract Base Class. Equivale a una interfaz de Java: define
    la firma de los métodos, pero no su implementación.
    """
    @abstractmethod
    def guardar(self, post: Post) -> Post:
        """Guarda (crea o actualiza) un post y lo devuelve con su Id asignado."""
    
    @abstractmethod
    def buscar_por_id(self, post_id: int) -> Optional[Post]:
        """Devuelve el post con el id dado, o None si no existe."""
    
    @abstractmethod
    def listar_publicados(self) -> List[Post]:
        """Devuelve todos los posts publicados."""

    @abstractmethod
    def eliminar(self, post_id: int) -> None:
        """Elimina el post con ese id."""

class UserRepository(ABC):
    """Puerto de salida: contrato de persistencia de usuarios."""
    
    @abstractmethod
    def guardar(self, user: User) -> User:
        """Guarda (crea o actualiza) un usuario y lo devuelve con su id."""
    
    @abstractmethod
    def buscar_por_id(self, user_id: int) -> Optional[User]:
        """Devuelve el usuario con ese id, o None si no existe."""
    
    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[User]:
        """Devuelve el usuario con ese email, o None si no existe.
        
        Necesario para el login: el usuario se identifica por email.
        """
    
class PasswordHasher(ABC):
    """Puerto de salida: contrato de hashing de contraseñas.

    NO es un repositorio: un puerto es cualquier capacidad externa que el
    dominio necesita. El dominio pide 'algo que sepa hashear', sin saber si
    detrás hay bcrypt, argon2 o pbkdf2.
    """

    @abstractmethod
    def hash(self, password: str) -> str:
        """Devuelve el hash de una contraseña en texto plano."""

    @abstractmethod
    def verify(self, password: str, password_hash: str) -> bool:
        """Comprueba si la contraseña corresponde al hash dado.

        Returns:
            bool: True si coincide, False si no.
        """