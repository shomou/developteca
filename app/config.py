"""
Configuración de la aplicación Developteca

Define clases de configuración por entorno (development | testing | production)
equivalente a los profiles de Spring. Cada clase lee sus valores desde 
variables de entorno cargadas por python-dotenv.
"""

import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    """ Configuración base: valores comines para todos los entornos """
    
    # Clave para firmar sesiones/cookies. Se lee de .env.
    SECRET_KEY = os.getenv('SECRET_KEY',  "clave-insegura-solo-dev")
    
    # URL de conexión a la base de datos.(Se usará por SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    # Desactiva un sistema de eventos de SQLAlchemy que no usamos (ahorra memoria)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    

class DevelopmentConfig(Config):
    """Entorno de desarrollo local: muestra errores detallados."""
    DEBUG = True
    
class TestingConfig(Config):
    """Entorno de pruebas: no muestra errores detallados."""
    TESTING = True
    
class ProductionConfig(Config):
    """Entorno de producción: no muestra errores detallados."""
    DEBUG = False
    TESTING = False
    

# Diccionario para elegir la config por nombre (lo usará el factory de Flask).
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}