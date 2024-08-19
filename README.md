# TC01 DockerRestAPI

# Gestor de Tareas con Flask y PostgreSQL

Este proyecto es una sistema para la gestión y autenticación de usuarios, así como para la publicación de diferentes tipos de posts.

## Funcionalidades principales 

- Autenticación de usuarios mediante JWT.
- Creación, actualización, lectura y eliminación de usuarios.
- Escritura de posts, tales como imágenes, textos y videos.
- Visualización de tareas por usuario y por ID de tarea.

## Herramientas principales usadas
- Python como lenguage principal para el backend.
- Fastapi como framework para la gestión del sistema.
- JWT para autenticación.
- Postman para la documentación de los endpoints.
- Doker y Dockercompose.
- Postgresql para la base de datos.

# Commandos 

## Construye y ejecuta el contenedor de docker
``` bash
docker-compose up --build
```

## Ejecutar el módulo de pruebas unitarias
``` bash

```

# Endpoints usando Postman

## Inicio de sesión
Se selecciona un método POST y se ingresa en un body de tipo raw el nombre de usuario y la contraseña.
### Request
``` bash
localhost:8000/login
```
### Body de ejemplo
``` bash
{
    "username": "juanpa05",
    "password": "1234"
}
```

## Registrar usuario
Se selecciona un método POST y se ingresa en un body de tipo raw el nombre de usuario, la contraseña, y el rol.
### Request
``` bash
localhost:8000/register
```
### Body de ejemplo
``` bash
{
    "username": "alex27",
    "password": "holamundo",
    "role": "editor"
}
```

## Obtener usuarios
Se selecciona un método GET.
### Request
``` bash
localhost:8000/read
```

## Eliminar usuario
Se selecciona un método DELETE y se ingresa en un body de tipo raw el id de usuario.
### Request
``` bash
localhost:8000/id/delete
```
### Body de ejemplo
``` bash
{
    "id": 10
}
```

## Actualizar usuario
Se selecciona un método PUT y se ingresa en un body de tipo raw el id de usuario, el nombre de usuario, la contraseña y el role.
### Request
``` bash
localhost:8000/id/update
```
### Body de ejemplo
``` bash
{
    "id" : 10,
    "username": "alex27",
    "password": "holamundo",
    "role": "editor"
}
```

## Escritura de posts
``` bash

```
