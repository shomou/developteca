"""
Caso de uso: crear un post.

Orquesta el dominio: construye la entidad Post (que valida sus propias
reglas) y la persiste a través del puerto PostRepository.
"""
from dataclasses import dataclass

from app.domain.entities import Post
from app.domain.ports import PostRepository


@dataclass(frozen=True)
class CreatePostCommand:
    """Datos de entrada del caso de uso (un DTO inmutable).

    Desacopla al caso de uso de cómo llegaron los datos (HTTP, CLI, tests).
    """

    title: str
    content: str
    author_id: int


class CreatePostUseCase:
    """Crea un nuevo post en estado borrador."""

    def __init__(self, post_repository: PostRepository) -> None:
        """Recibe el repositorio por INYECCIÓN DE DEPENDENCIAS.

        Args:
            post_repository: cualquier implementación del puerto. El caso de
                uso depende de la abstracción, nunca de una clase concreta.
        """
        self._posts = post_repository

    def execute(self, command: CreatePostCommand) -> Post:
        """Ejecuta el caso de uso.

        Args:
            command: los datos del post a crear.

        Returns:
            Post: el post creado, ya con su id asignado.

        Raises:
            InvalidPostError: si los datos violan las reglas del dominio.
        """
        # 1. Construir la entidad: ella valida sus propias invariantes.
        post = Post(
            title=command.title,
            content=command.content,
            author_id=command.author_id,
        )
        # 2. Persistir a través del puerto.
        return self._posts.guardar(post)