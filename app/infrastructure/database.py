"""
Instancia central de SQLAlchemy.

Se crea aquí, sin app, y se conecta a la app dentro del factory con
db.init_app(app). Este patrón (extensión sin app) permite tener varias
apps/configuraciones -justo lo que necesitabamos para los tests-
"""
from flask_sqlalchemy import SQLAlchemy

# Aún no está atada a ninguna app: eso ocurre en create_app().
db = SQLAlchemy()