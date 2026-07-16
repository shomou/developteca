"""
Caso de uso: eliminar un post.
"""
from app.domain.exceptions import PostNotFoundError
from app.domain.ports import PostRepository

class DeletePostUseCase:
    """Eliminar un post existente en el blog."""
    
    def __init__(self, post_repository: PostRepository) -> None:
        """Recibe el puerto por inyección de dependencias."""
        self._posts = post_repository
    
    def execute(self, post_id: int) -> None:
        """Ejecuta el caso de uso.

        Args:
            post_id: id del post a eliminar.

        Raises:
            PostNotFoundError: si no existe un post con ese id.
        """
        # Verificamos que existe ANTES de borrar
        post = self._posts.buscar_por_id(post_id)
        if post is None:
            raise PostNotFoundError(f"No existe un post con id {post_id}")
        
        self._posts.eliminar(post_id)
        