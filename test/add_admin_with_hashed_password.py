# add_admin_with_hashed_password.py
# Script de utilidad para añadir un usuario administrador con una contraseña ya hasheada a la base de datos.

import logging
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Añadir el directorio raíz del proyecto al PATH de Python
# Esto es crucial cuando se ejecuta un script que está anidado en una subcarpeta
# y necesita importar módulos de otras subcarpetas de la raíz del proyecto.
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir)) # Sube un nivel para llegar a pizzeria_web
if project_root not in sys.path:
    sys.path.append(project_root)

# Importa la configuración de la base de datos
from core.config import settings # Asumiendo que config.py está directamente en la raíz de pizzeria_web
# SI config.py está en core/, entonces sería: from core.config import settings

# Importa el modelo base y el modelo Administrador
# Si tus modelos están en core/models.py, la importación sería: from core.models import Base, Administrador
from models.models import Base, Administrador # Asumiendo que core/models.py existe

# Importa el servicio de Administrador
from services.administrador_service import AdministradorService

# Configuración del Logger (similar a main.py)
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def add_hashed_admin_to_db(hashed_password_from_user: str, username: str, email: str = None, super_admin: bool = False):
    """
    Añade un nuevo administrador a la base de datos con una contraseña ya hasheada.

    Args:
        hashed_password_from_user (str): La contraseña ya hasheada (obtenida de bcrypt).
        username (str): El nombre de usuario para el administrador.
        email (str, optional): El correo electrónico del administrador. Defaults to None.
        super_admin (bool, optional): True si es un super administrador. Defaults to False.
    """
    logger.info("Iniciando el script para añadir administrador con contraseña hasheada...")

    try:
        # Configuración de la base de datos
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(engine) # Asegura que las tablas existan
        Session = sessionmaker(bind=engine)
        logger.info("Conexión a la base de datos establecida.")
    except SQLAlchemyError as e:
        logger.critical(f"Error crítico al conectar o inicializar la base de datos: {e}")
        return # Sale si hay un error de conexión

    admin_service = AdministradorService(Session)

    # Opcional: Verificar si el usuario ya existe para evitar duplicados
    existing_admin = admin_service.get_administrador_by_usuario(username)
    if existing_admin:
        logger.warning(f"El usuario '{username}' ya existe. No se añadió un nuevo administrador.")
        return

    logger.info(f"Intentando añadir administrador '{username}' con contraseña hasheada...")
    
    # Crea una instancia del modelo Administrador directamente con el hash proporcionado.
    nuevo_admin_con_hash = Administrador(
        usuario=username,
        contrasena_hash=hashed_password_from_user,
        email=email,
        super_admin=super_admin
    )

    # Usa el método 'add' de BaseService (que AdministradorService hereda)
    # para insertar directamente esta instancia del modelo.
    added_admin = admin_service.add(nuevo_admin_con_hash)

    if added_admin:
        logger.info(f"Administrador '{added_admin.usuario}' (ID: {added_admin.id}) añadido con éxito.")
        logger.info(f"Hash de contraseña almacenado: {added_admin.contrasena_hash}")
        # Puedes añadir aquí una prueba de verificación si lo deseas, usando la contraseña
        # en texto plano original que generó el hash.
    else:
        logger.error(f"Fallo al añadir el administrador '{username}'. Consulta los logs para más detalles.")

if __name__ == "__main__":
    # --- ¡IMPORTANTE! Reemplaza esto con tu hash real de bcrypt ---
    # Este es solo un ejemplo. Usa el hash que obtuviste de tu notebook (hash_password.ipynb).
    # Ejemplo: "$2b$12$EjemploDeHashRealDeBcryptGeneradoPreviamentePorTi.QWEasd.123"
    YOUR_HASHED_PASSWORD = "$2b$12$AWlxuyjdYM9XVgCY1mdMw.Qu5YJNMpt.SbdZMVev6VWAwQgWdBApq" # Reemplaza con tu hash
    
    # Define los detalles para el nuevo usuario administrador
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "kerwin27120201@gmail.com"
    IS_SUPER_ADMIN = True # Establece a True si este debe ser un super administrador

    # Llama a la función para añadir el administrador
    add_hashed_admin_to_db(YOUR_HASHED_PASSWORD, ADMIN_USERNAME, ADMIN_EMAIL, IS_SUPER_ADMIN)

    # Puedes ejecutar este script varias veces con diferentes hashes y usuarios
    # si necesitas añadir múltiples administradores predefinidos.
