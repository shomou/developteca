"""
Punto de entrada para desarrollo local

Ejecuta el servidor de desarrollo Flask. En producción no se usa esto
(se usa wsgi.py con un servidor como Gunicorn/Waitress).
"""
from app import create_app

app = create_app()  # Crea la app con la configuración según FLASK_ENV

if __name__ == "__main__":
    # host y puerto por defecto: 127.0.0.1:5000
    app.run(debug=True)
