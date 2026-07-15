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

