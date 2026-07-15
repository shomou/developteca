"""
Application Factory de Developteca.

Expone create_app(): construye y configura la instancia de Flask según el
entorno (development/testing/production). Es el punto de ensamblaje de la app,
equivalente a una clase @Configuration que arma el contexto en Spring.
"""
import os
from flask import Flask

from app.config import config_by_name

def create_app(config_name=None):
    """Crea y configura una instancia de la aplicación Flask.

    Args:
        config_name: nombre del entorno ('development', 'testing',
            'production'). Si es None, se toma de la variable FLASK_ENV.

    Returns:
        Flask: la aplicación ya configurada y lista para usar.
    """
    # 1. Decide qué configuración usar (perfil).
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    
    # 2. Crea la instancia de Flask.
    app = Flask(__name__)
    
    # 3. Carga la clase de configuración correspondiente al entorno.
    app.config.from_object(config_by_name[config_name])
    
    # 4. Ruta temporal de prueba para confirmar que la app arranca.
    @app.route("/health")
    def health():
        """Endpoint de salud. Confirma que la app responde"""
        return {"status": "ok", "app": "Developteca"}, 200
    
    return app