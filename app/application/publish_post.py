"""
Caso de uso: publicar un post existente.

Flujo: busca el post por id, le pide publicarse (la entidad aplica sus
propias reglas) y persiste el cambio.
"""
from app.domain.entities import Post
from app.domain.exceptions import PostNotFoundError
from app.domain.ports import PostRepository

class PublishPostUseCase:
    """Publica un post que ya existe en el repositorio."""
    
    def __init__(self, post_repository: PostRepository) -> None:
        """Recibe el repositorio por INYECCIÓN DE DEPENDENCIAS."""
        self._posts = post_repository
    
    def execute(self, post_id: int) -> Post:
        """Ejecuta el caso de uso.

        Args:
            post_id: id del post a publicar.

        Returns:
            Post: el post ya publicado.

        Raises:
            PostNotFoundError: si no existe un post con ese id.
            PostAlreadyPublishedError: si el post ya estaba publicado.
            InvalidPostError: si el post no tiene contenido.
        """
        # 1. LEER
        post = self._posts.buscar_por_id(post_id)
        if post is None:
            raise PostNotFoundError(f"No existe un post con id {post_id}.")
        # 2. MUTAR
        post.publicar()
        
        # 3. PERSISITIR
        return self._posts.guardar(post)
    