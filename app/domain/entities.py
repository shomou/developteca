"""
Entidades del dominio de Developteca

Una entidad tiene identidad propia (id) y estado mutable y encapsula 
reglas de negocio que la gobiernan. Python puro sin Flask ni SQLAlchemy.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from app.domain.exceptions import InvalidPostError, PostAlreadyPublishedError, InvalidUserError

from app.domain.value_objects import Email

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
    
    def __post_init__(self) -> None:
        """Valida las invariantes al crear el post."""
        self._validar_titulo(self.title)
    
    @staticmethod
    def _validar_titulo(title: str) -> None:
        """Valida el título. Compartido por la creación y la edición.

        Raises:
            InvalidPostError: si el título está vacío o solo tiene espacios.
        """
        if not title or not title.strip():
            raise InvalidPostError("El título no puede estar vacío")
    
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
    
    def actualizar(self, title: str, content: str) -> None:
        """Actualiza el título y el contenido del post.

        Editar NO cambia el estado: un post publicado sigue publicado.

        Reglas de negocio:
        - El título nunca puede quedar vacío.
        - Un post publicado no puede quedarse sin contenido (rompería la
          garantía que estableció publicar()).

        Args:
            title: nuevo título.
            content: nuevo contenido en Markdown.

        Raises:
            InvalidPostError: si se viola alguna de las reglas anteriores.
        """
        self._validar_titulo(title)

        if self.esta_publicado and (not content or not content.strip()):
            raise InvalidPostError(
                "Un post publicado no puede quedarse sin contenido"
            )

        self.title = title
        self.content = content    
        
@dataclass(eq=False)
class User:
    """Un usuario del panel de administración.
    
    Nota: guarda password_hash, NUNCA la contraseña en texto plano.
    La entidad no sabe COMO se hashea: eso es tarea del puerto PasswordHasher
    """
    
    username: str
    email: Email
    password_hash: str
    id: Optional[int] = None
    created_at: datetime = field(default_factory=lambda: datetime.now)
    
    def __post_init__(self) -> None:
        """Valida las invariantes al crear el usuario."""
        if not self.username or not self.username.strip():
            raise InvalidUserError("El username no puede estar vacio")
        if not isinstance(self.email, Email):
            raise InvalidUserError("El email debe ser un Value Object")
        if not self.password_hash:
            raise InvalidUserError("El usuario debe tener un password_hash")
    
    def __eq__(self, other: object) -> bool:
        """Igualdad por IDENTIDAD, como en Post."""
        if not isinstance(other, User):
            return NotImplemented
        if self.id is None or other.id is None:
            return self is other
        return self.id == other.id
    
    