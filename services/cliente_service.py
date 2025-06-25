# services/cliente_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from models.models import Cliente # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService

class ClienteService(BaseService):
    """
    Servicio para gestionar operaciones CRUD y de búsqueda para el modelo Cliente.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    def add_cliente(self, cliente_data: dict):
        """
        Añade un nuevo cliente a la base de datos.

        Args:
            cliente_data (dict): Diccionario con los datos del cliente.
                                 Ej: {'nombre': 'Juan Perez', 'email': 'juan@example.com', 'direccion': 'Calle Falsa 123'}

        Returns:
            Cliente: La instancia del cliente añadida.
            None: Si ocurre un error.
        """
        nuevo_cliente = Cliente(**cliente_data)
        return self.add(nuevo_cliente)

    def get_cliente_by_id(self, cliente_id: int):
        """Obtiene un cliente por su ID."""
        return self.get_by_id(Cliente, cliente_id)

    def search_clientes(self, query: str):
        """
        Busca clientes por nombre, email o teléfono.

        Args:
            query (str): El término de búsqueda.

        Returns:
            list[Cliente]: Una lista de clientes que coinciden con la búsqueda.
        """
        session: Session = self.Session()
        try:
            return session.query(Cliente).filter(
                or_(
                    Cliente.nombre.ilike(f'%{query}%'),
                    Cliente.email.ilike(f'%{query}%'),
                    Cliente.telefono.ilike(f'%{query}%')
                )
            ).all()
        except SQLAlchemyError as e:
            print(f"Error al buscar clientes con query '{query}': {e}")
            return None
        finally:
            session.close()

    def get_cliente_by_email(self, email: str):
        """
        Obtiene un cliente por su dirección de correo electrónico.

        Args:
            email (str): El correo electrónico a buscar.

        Returns:
            Cliente: La instancia del cliente si se encuentra, None en caso contrario.
        """
        session: Session = self.Session()
        try:
            return session.query(Cliente).filter_by(email=email).first()
        except SQLAlchemyError as e:
            print(f"Error al buscar cliente por email '{email}': {e}")
            return None
        finally:
            session.close()

    def update_cliente(self, cliente_instance: Cliente):
        """Actualiza un cliente existente."""
        return self.update(cliente_instance)

    def delete_cliente(self, cliente_instance: Cliente):
        """Elimina un cliente."""
        return self.delete(cliente_instance)

    def get_all_clientes(self):
        """Obtiene todos los clientes."""
        return self.get_all(Cliente)
