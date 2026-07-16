"""
Caso de uso: listar todos los posts publicados del blog.

Es una 'query': solo lee, no modifica nada
"""
from typing import List

from app.domain.entities import Post
from app.domain.ports import PostRepository

class ListPostsUseCase:
    """Devuelve los posts visibles en el blog público (los publicados)."""
    
    def __init__(self, post_repository: PostRepository) -> None:
        """Recibe el puerto por inyección de dependencias."""
        self._posts = post_repository
    
    def execute(self) -> List[Post]:
        """Devuelve todos los posts publicados.

        Returns:
            List[Post]: lista de posts publicados.
        """
        return self._posts.listar_publicados()