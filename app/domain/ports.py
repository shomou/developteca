"""
Puertos (interfaces) del dominio Developteca.

Un puerto declara QUÉ necesita el dominio del mundo exterior, sin decir CÓMO
se implementa. La infraestructura proveerá los adaptadores concretos.
Aquí NO se menciona SQLAlchemy, PostgreSQL ni Flask: solo el contrato.
"""
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Post

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