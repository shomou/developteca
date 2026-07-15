"""
Value Objects del dominio de Developteca.

Un Value Object es inmutable y se compara por su valor, no por identidad.
Su validez queda garantizada en el momento de crearlo.
"""
import re
from dataclasses import dataclass

from app.domain.exceptions import InvalidEmailError

#Patrón simple: texto@texto (sin espacions ni arrobas de más)
_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")    

@dataclass(frozen=True)
class Email:
    """Representa un correo electrónico válido.
    frozen=True los hace inmutables (no se pueden cambiar sus atributos después de crearlo).
    dataclass genera automáticamente __init__, __repr__, __eq__ y otros métodos.
    """
    value: str
    
    def __post_init__(self) -> None:
        """Se ejecuta justo después de crear el objeto: valida el formato."""
        if not _EMAIL_REGEX.match(self.value):
            raise InvalidEmailError(f"Email inválido: {self.value!r}")


