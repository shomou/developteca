"""
Excepciones del dominio de Developteca.

Representan violaciones de reglas de negocio, independientes de la
infraestructura (BD, HTTP). Todas heredan de DomainError.
"""


class DomainError(Exception):
    """Excepción base para todos los errores del dominio."""


class InvalidEmailError(DomainError):
    """Se lanza cuando un email no cumple el formato válido."""

class InvalidPostError(DomainError):
    """Se lanza cuando un post no cumple con las reglas de negocio."""

class PostAlreadyPublishedError(DomainError):
    """Se lanza cuando se intenta publicar un post que ya está publicado."""

class PostNotFoundError(DomainError):
    """Se lanza cuando no existe un post con el id solicitado."""

class InvalidUserError(DomainError):
    """Se lanza cuando un usuario no cumple con las reglas de negocio."""
    
class UserNotFoundError(DomainError):
    """Se lanza cuando no existe el usuario solicitado"""

class InvalidCredentialsError(DomainError):
    """Se lanza cuando las credenciales de acceso son incorrectas."""