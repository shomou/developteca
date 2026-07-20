"""
Model SQLAlchemy: el mapeo objeto-relacional de las tablas.

OJO: estas clases son de INFRAESTRUCTURA, no de dominio. Representan filas
de tablas, no reglas de negocio. No confundir con app/domain/entities.py.
"""
from datetime import datetime, timezone

from app.infrastructure.database import db

class PostModel(db.Model):
    """Tabla 'posts'. Mapea ña entidad de dominio Post"""
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(200), nullable=False, default="draft")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)

class UserModel(db.Model):
    """Tabla 'users'. Mapea la entidad de dominio User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
