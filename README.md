# Proyecto Emaús

Aplicación web en Flask para rezar el Rosario y la Divina Misericordia con inicio de sesión y cambio de fondo.

## Requisitos

- Python 3.10 o superior
- Flask
- Flask-SQLAlchemy
- Werkzeug

## Instalación

1. Crear y activar un entorno virtual:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python app.py
```

Luego abrir `http://127.0.0.1:5000` en el navegador.

## Acceso

- Usuario: `admin`
- Contraseña inicial: `3132`

## Estructura básica

- `app.py` - aplicación principal de Flask
- `htmls/` - plantillas HTML
- `cosas/` - archivos estáticos y estilos
- `info/` - datos del rosario y la coronilla
- `instance/` - carpeta de configuración privada para Flask (ignoradas por Git)

## Notas

- El proyecto crea la base de datos `users.db` automáticamente al iniciar.
- El archivo `cosas/uploads/fondo_actual.txt` se usa para guardar el fondo seleccionado por el usuario.
