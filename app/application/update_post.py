"""
Caso de uso: actualizar un post existente.

Flujo: busca el post, le pide actualizarse (la entidad aplica sus reglas)
y persiste el cambio. Mismo patrón leer → mutar → persistir.
"""
from dataclasses import dataclass

from app.domain.entities import Post
from app.domain.exceptions import PostNotFoundError
from app.domain.ports import PostRepository


@dataclass(frozen=True)
class UpdatePostCommand:
    """Datos de entrada: qué post editar y con qué valores."""

    post_id: int
    title: str
    content: str


class UpdatePostUseCase:
    """Actualiza el título y el contenido de un post existente."""

    def __init__(self, post_repository: PostRepository) -> None:
        """Recibe el puerto por inyección de dependencias."""
        self._posts = post_repository

    def execute(self, command: UpdatePostCommand) -> Post:
        """Ejecuta el caso de uso.

        Args:
            command: id del post y los nuevos valores.

        Returns:
            Post: el post ya actualizado.

        Raises:
            PostNotFoundError: si no existe un post con ese id.
            InvalidPostError: si los nuevos valores violan las reglas.
        """
        # 1. LEER
        post = self._posts.buscar_por_id(command.post_id)
        if post is None:
            raise PostNotFoundError(f"No existe un post con id {command.post_id}")

        # 2. MUTAR: las reglas viven en la entidad.
        post.actualizar(title=command.title, content=command.content)

        # 3. PERSISTIR
        return self._posts.guardar(post)
