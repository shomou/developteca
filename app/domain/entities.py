"""
Entidades del dominio de Developteca

Una entidad tiene identidad propia (id) y estado mutable y encapsula 
reglas de negocio que la gobiernan. Python puro sin Flask ni SQLAlchemy.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from app.domain.exceptions import InvalidPostError, PostAlreadyPublishedError

class PostStatus(Enum):
    """Enum que representa el estado de un post."""
    DRAFT = "draft"
    PUBLISHED = "published"

@dataclass(eq=False)
class Post:
    """Un articulo del blog.
    eq=False No queremos la igualdad por valor que genera dataclass.
    Las entidades se comparan por identidad (id) y no por valor.
    """
    title: str
    content: str
    author_id: str
    id: Optional[int] = None
    status: PostStatus = PostStatus.DRAFT
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    published_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Valida las invarientes al crear post."""
        if not self.title or not self.title.strip():
            raise InvalidPostError("El título no puede estar vacío.")
    
    def __eq__(self, other: object) -> bool:
        """Igualdad por IDENTIDAD: dos posts son iguales si tienen el mismo id."""
        if not isinstance(other, Post):
            return NotImplemented
        # Sin id (aun no persistidos)  =>  solo es igual asi mismo.
        if self.id is None or other.id is None:
            return self is other
        return self.id == other.id  
    
    @property
    def esta_publicado(self) -> bool:
        """True si el post ya fue publicado"""
        return self.status is PostStatus.PUBLISHED
    
    def publicar(self):
        """Publica el post.
        
        Reglas del negocio:
        - Un post publicado no puede publicarse de nuevo
        - Un post sin contenido no puede publicarse
        
        Raises:
            PostAlreadyPublishedError: Si el post ya fue publicado.
            InvalidPostError: Si el post no tiene contenido.
        """
        if self.status is PostStatus.PUBLISHED:
            raise PostAlreadyPublishedError("El post ya fue publicado.")
        
        if not self.content or not self.content.strip():
            raise InvalidPostError("El post no puede publicarse sin contenido.")
        
        self.status = PostStatus.PUBLISHED
        self.published_at = datetime.now(timezone.utc)
        
        
        