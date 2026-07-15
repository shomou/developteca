# Developteca — Contexto del Proyecto

Blog profesional con consola de administración, construido **desde cero** con
arquitectura hexagonal. Este archivo lo lee Claude automáticamente: define qué es
el proyecto y **cómo debe trabajar Claude conmigo**.

## 🎯 Objetivo

Crear un blog open source con panel de administración, siguiendo arquitectura
hexagonal (puertos y adaptadores), con testing desde el inicio y código profesional.

## 🧑‍💻 Cómo debe trabajar Claude conmigo (IMPORTANTE)

- **No sé Python ni Flask, y quiero aprender haciéndolo yo mismo.**
- Claude **NO** debe escribir/crear los archivos de código del proyecto por mí.
  Claude me da las instrucciones y el código para que **yo lo escriba/pegue y ejecute**.
- **Explicar el concepto ANTES del código**: qué hacemos, por qué en hexagonal,
  y su relación con Java (vengo de ese mundo).
- Trabajamos en **sesiones cortas** según el tiempo que yo tenga ese día
  (ej. "hoy solo tengo 15 min"). Claude pregunta/considera el tiempo disponible.
- Estoy **cómodo con la terminal** (PowerShell, Windows). No hace falta explicar
  comandos básicos tecla por tecla, pero sí explicar qué hace cada comando nuevo.
- Cada sesión termina con un **checklist**: ✓ lo completado y ➜ el siguiente paso.
- Diagnóstico/verificación del entorno SÍ lo puede hacer Claude (revisar versiones,
  rutas, estructura). Lo que no hace es construir el proyecto por mí.
- No copiar/pegar a ciegas: entender qué hace cada línea.

## 🛠️ Stack técnico

- **Lenguaje/Framework**: Python 3.10+ · Flask 2.3+
- **Base de datos**: PostgreSQL (obligatorio) · SQLAlchemy
- **Arquitectura**: Hexagonal (puertos y adaptadores)
- **Formato de posts**: Markdown
- **Frontend**: Bootstrap 5 (CDN) · Vanilla JavaScript
- **Dependencias previstas**: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Login,
  psycopg2-binary, python-dotenv, marshmallow, python-slugify, pytest, pytest-cov

## 📁 Estructura hexagonal

```
developteca/
├── app/
│   ├── domain/          # CORE — Entidades y Puertos (no depende de nada externo)
│   ├── application/     # Casos de Uso
│   ├── infrastructure/  # Adaptadores de Salida (BD, seguridad, etc.)
│   ├── interfaces/      # Adaptadores de Entrada (HTTP, CLI)
│   └── config.py
├── tests/               # Unit, Integration, E2E
├── migrations/          # Alembic para versionamiento de BD
├── requirements.txt
├── run.py
└── wsgi.py
```

## 💻 Entorno local (verificado)

- Python 3.11.9 ✅ · pip 24.0 ✅ · Git 2.45.1 ✅
- PostgreSQL 17 instalado en `C:\Program Files\PostgreSQL\17` pero **NO en PATH** ❌
  (pendiente agregarlo cuando toque configurar la base de datos).
- Entorno virtual: `venv\` (activar con `.\venv\Scripts\Activate.ps1`).

## 🚀 Fases del proyecto

1. Configuración base (estructura, Flask factory, PostgreSQL, migrations, testing)
2. Core de dominio (entidades User/Post/Category, value objects, excepciones, puertos)
3. Casos de uso (Create/Publish/Update/Delete/List Post, Authenticate)
4. Adaptadores de salida (repositorios SQLAlchemy, password hasher, modelos, migrations)
5. Adaptadores de entrada (controllers, presenters, validators, blueprints)
6. Interfaz de administración (templates, JS, integración API)
7. Interfaz pública del blog (templates, listado/vista de posts, búsqueda/categorías)
8. Testing completo (unit, integración, E2E, coverage > 80%)

## 📌 Progreso actual

- **Sesión 1 — ✅ COMPLETADA**: esqueleto creado (venv + estructura de carpetas
  hexagonal + archivos base vacíos).
- **Sesión 2 — ✅ COMPLETADA**: `requirements.txt` lleno e instalado en el venv (10
  libs + deps). Nota: se instaló Werkzeug 3.1.8 con Flask 2.3.3 — vigilar posibles
  errores de werkzeug al arrancar Flask.
- **Sesión 3 — ✅ COMPLETADA**: configuración lista — `.gitignore` (protege `.env` y
  `venv/`), `.env` (SECRET_KEY generada, DATABASE_URL a postgres) y `app/config.py`
  (clases Config por entorno + `config_by_name`). Prueba de carga OK.
  ⚠️ La BD se llama **`developteca_db`** (usuario `postgres`, puerto 5432) — hay que
  crearla con ese nombre exacto.
- **Sesión 4 — ✅ COMPLETADA**: PostgreSQL 17 agregado al PATH de usuario; BD
  `developteca_db` creada; `app/__init__.py` con `create_app()` (factory que lee
  `config_by_name` + ruta temporal `/health`); `run.py` (arranca `app.run(debug=True)`).
  Flask arranca y `/health` devuelve `{"status":"ok","app":"Developteca"}`. Sin error
  de Werkzeug. Fin de la Fase 1 (Configuración base).
- **Sesión 5 — ➜ SIGUIENTE**: Fase 2 (Core de dominio). Empezar por la entidad `Post`
  (o `User`) y un value object (ej. `Email`/`Slug`) en `app/domain/`, con sus tests
  unitarios. Aún SIN Flask/SQLAlchemy: dominio puro de Python.
