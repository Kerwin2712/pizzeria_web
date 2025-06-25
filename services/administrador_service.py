# services/administrador_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import Administrador # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService
import bcrypt # Necesitarás instalar bcrypt: pip install bcrypt

class AdministradorService(BaseService):
    """
    Servicio para gestionar operaciones CRUD y de búsqueda para el modelo Administrador.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    def hash_password(self, password: str) -> str:
        """
        Genera un hash de la contraseña usando bcrypt.

        Args:
            password (str): La contraseña en texto plano.

        Returns:
            str: El hash de la contraseña codificado.
        """
        # Generar un salt y hashear la contraseña
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifica una contraseña en texto plano contra un hash.

        Args:
            password (str): La contraseña en texto plano.
            hashed_password (str): La contraseña hasheada almacenada.

        Returns:
            bool: True si la contraseña coincide, False en caso contrario.
        """
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except ValueError:
            # Manejar el caso donde el hash no es válido
            return False

    def add_administrador(self, usuario: str, contrasena: str, email: str = None, super_admin: bool = False):
        """
        Añade un nuevo administrador, hasheando la contraseña.

        Args:
            usuario (str): Nombre de usuario del administrador.
            contrasena (str): Contraseña en texto plano.
            email (str, optional): Correo electrónico del administrador. Defaults to None.
            super_admin (bool, optional): Si es super administrador. Defaults to False.

        Returns:
            Administrador: La instancia del administrador añadida.
            None: Si ocurre un error.
        """
        hashed_contrasena = self.hash_password(contrasena)
        nuevo_admin = Administrador(
            usuario=usuario,
            contrasena_hash=hashed_contrasena,
            email=email,
            super_admin=super_admin
        )
        return self.add(nuevo_admin)

    def get_administrador_by_id(self, admin_id: int):
        """Obtiene un administrador por su ID."""
        return self.get_by_id(Administrador, admin_id)

    def get_administrador_by_usuario(self, usuario: str):
        """
        Busca un administrador por su nombre de usuario.

        Args:
            usuario (str): El nombre de usuario a buscar.

        Returns:
            Administrador: La instancia del administrador si se encuentra, None en caso contrario.
        """
        session: Session = self.Session()
        try:
            return session.query(Administrador).filter_by(usuario=usuario).first()
        except SQLAlchemyError as e:
            print(f"Error al buscar administrador por usuario '{usuario}': {e}")
            return None
        finally:
            session.close()

    def get_administrador_by_email(self, email: str):
        """
        Busca un administrador por su correo electrónico.

        Args:
            email (str): El correo electrónico a buscar.

        Returns:
            Administrador: La instancia del administrador si se encuentra, None en caso contrario.
        """
        session: Session = self.Session()
        try:
            return session.query(Administrador).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error al buscar administrador por email '{email}': {e}")
            return None
        finally:
            session.close()

    def update_administrador(self, admin_instance: Administrador):
        """Actualiza un administrador existente."""
        # Nota: Si la contraseña necesita ser actualizada, se debe hashear antes de pasar la instancia.
        return self.update(admin_instance)

    def delete_administrador(self, admin_instance: Administrador):
        """Elimina un administrador."""
        return self.delete(admin_instance)

    def get_all_administradores(self):
        """Obtiene todos los administradores."""
        return self.get_all(Administrador)
