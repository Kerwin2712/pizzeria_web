# pizzeria_web
Pagina web para una pizzeria

# Instalación

Clona el repositorio.
Instala los requerimientos.
Crea la base de datos.
Carga las tablas.
Crea el archivo .env con las variables de entorno.

1. Instalar psql
2. Ingresar al servidor: psql -U postgres
3. Crear la base de datos: CREATE DATABASE tu_base_de_datos;
4. Crear un nuevo usuario: createuser -U postgres --interactive
5. El comando --interactive te guiará con preguntas:
	-Enter name of role to add: (Introduce el nombre del rol a añadir): Aquí escribes el nombre del nuevo usuario que quieres crear (tu_usuario).
	-Shall the new role be a superuser? (y/n) (¿Debe el nuevo rol ser un superusuario?): Generalmente, n (no) por razones de seguridad, a menos que realmente necesites que tenga permisos de superusuario.
	-Shall the new role be allowed to create databases? (y/n) (¿Debe el nuevo rol poder crear bases de datos?): Si este usuario va a crear bases de datos (como tu aplicación), escribe y. Si solo se va a conectar a una base de datos ya existente, n.
	-Shall the new role be allowed to create new roles? (y/n) (¿Debe el nuevo rol poder crear nuevos roles/usuarios?): Generalmente n.
6. Asignar una contraseña al usuario: 
	-psql -U postgres
	-ALTER USER tu_usuario WITH PASSWORD 'tu_contraseña_segura';
    -GRANT CREATE ON SCHEMA public TO tu_usuario;
    -GRANT ALL PRIVILEGES ON DATABASE tu_base_de_datos TO tu_usuario;
7. Cargar las tablas: psql -U tu_usuario -d tu_base_de_datos -f backup.sql (ir a la carpeta contenedora en core).
8. Revisar que esten las tablas:
	-psql -U tu_usuario -d tu_base_de_datos
	-\d
9. crea tu archivo .env con las variables de entorno:
    DATABASE_URL=postgresql://tu_usuario:tu_contraseña_segura@localhost:5432/tu_base_de_datos
    DB_HOST = 'localhost'
    DB_NAME = 'tu_base_de_datos'
    DB_USER = 'tu_usuario'
    DB_PASSWORD = 'tu_contraseña_segura'
    DB_PORT = '5432'
10. Inicia la pagina web con: python main.py
