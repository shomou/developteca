"""
Dobles de prueba (fakes) que implementan los puertos del dominio.

Un 'fake' es una implementación real pero simplificada del contrato:
mismo comportamiento, con un diccionario en vez de PostgreSQL.
"""
from typing import Dict, List, Optional

from app.domain.entities import Post, User
from app.domain.ports import PostRepository, UserRepository, PasswordHasher


class InMemoryPostRepository(PostRepository):
    """Implementación en memoria del puerto PostRepository."""

    def __init__(self) -> None:
        self._posts: Dict[int, Post] = {}
        self._siguiente_id = 1

    def guardar(self, post: Post) -> Post:
        """Asigna un id si el post es nuevo y lo almacena."""
        if post.id is None:
            post.id = self._siguiente_id
            self._siguiente_id += 1
        self._posts[post.id] = post
        return post

    def buscar_por_id(self, post_id: int) -> Optional[Post]:
        return self._posts.get(post_id)

    def listar_publicados(self) -> List[Post]:
        return [p for p in self._posts.values() if p.esta_publicado]

    def eliminar(self, post_id: int) -> None:
        self._posts.pop(post_id, None)

class InMemoryUserRepository(UserRepository):
    """Implementación en memoria del puerto UserRepository."""

    def __init__(self) -> None:
        self._users: Dict[int, User] = {}
        self._siguiente_id = 1

    def guardar(self, user: User) -> User:
        if user.id is None:
            user.id = self._siguiente_id
            self._siguiente_id += 1
        self._users[user.id] = user
        return user

    def buscar_por_id(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def buscar_por_email(self, email: str) -> Optional[User]:
        for user in self._users.values():
            if user.email.value == email:
                return user
        return None


class FakePasswordHasher(PasswordHasher):
    """Hasher de mentira para tests: rápido y predecible.

    ⚠️ SOLO PARA TESTS. Es trivialmente reversible.
    El adaptador real usará bcrypt (Fase 4).
    """

    def hash(self, password: str) -> str:
        return f"hashed::{password}"

    def verify(self, password: str, password_hash: str) -> bool:
        return password_hash == self.hash(password)