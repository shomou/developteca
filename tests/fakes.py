"""
Dobles de prueba (fakes) que implementan los puertos del dominio.

Un 'fake' es una implementación real pero simplificada del contrato:
mismo comportamiento, con un diccionario en vez de PostgreSQL.
"""
from typing import Dict, List, Optional

from app.domain.entities import Post
from app.domain.ports import PostRepository


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