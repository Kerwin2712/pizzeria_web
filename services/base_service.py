# services/base_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

class BaseService:
    """
    Clase base para los servicios de base de datos.
    Gestiona las operaciones CRUD básicas y el manejo de sesiones.
    """
    def __init__(self, Session: sessionmaker):
        """
        Inicializa el servicio con una fábrica de sesiones de SQLAlchemy.

        Args:
            Session (sessionmaker): La fábrica de sesiones de SQLAlchemy.
        """
        self.Session = Session

    def add(self, model_instance):
        """
        Añade una nueva instancia de modelo a la base de datos.

        Args:
            model_instance: La instancia del modelo (ej. Cliente, ItemMenu) a añadir.

        Returns:
            model_instance: La instancia del modelo añadida con su ID.
            None: Si ocurre un error.
        """
        session: Session = self.Session()
        try:
            session.add(model_instance)
            session.commit()
            session.refresh(model_instance) # Asegura que la instancia tenga el ID generado
            return model_instance
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al añadir {model_instance.__class__.__name__}: {e}")
            return None
        finally:
            session.close()

    def get_by_id(self, model_class, id: int):
        """
        Obtiene una instancia de modelo por su ID.

        Args:
            model_class: La clase del modelo (ej. Cliente, ItemMenu).
            id (int): El ID de la instancia a buscar.

        Returns:
            model_instance: La instancia encontrada.
            None: Si no se encuentra o ocurre un error.
        """
        session: Session = self.Session()
        try:
            return session.query(model_class).get(id)
        except SQLAlchemyError as e:
            print(f"Error al obtener {model_class.__name__} por ID {id}: {e}")
            return None
        finally:
            session.close()

    def update(self, model_instance):
        """
        Actualiza una instancia de modelo existente en la base de datos.
        La instancia debe tener un ID válido.

        Args:
            model_instance: La instancia del modelo a actualizar.

        Returns:
            model_instance: La instancia actualizada.
            None: Si ocurre un error.
        """
        session: Session = self.Session()
        try:
            session.merge(model_instance) # merge maneja si la instancia está detached o no
            session.commit()
            session.refresh(model_instance)
            return model_instance
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al actualizar {model_instance.__class__.__name__} (ID: {model_instance.id}): {e}")
            return None
        finally:
            session.close()

    def delete(self, model_instance):
        """
        Elimina una instancia de modelo de la base de datos.

        Args:
            model_instance: La instancia del modelo a eliminar.

        Returns:
            bool: True si la eliminación fue exitosa, False en caso contrario.
        """
        session: Session = self.Session()
        try:
            # Re-adjuntar la instancia a la sesión si está detached
            session.delete(session.merge(model_instance))
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al eliminar {model_instance.__class__.__name__} (ID: {model_instance.id}): {e}")
            return False
        finally:
            session.close()

    def get_all(self, model_class):
        """
        Obtiene todas las instancias de un modelo.

        Args:
            model_class: La clase del modelo.

        Returns:
            list: Una lista de todas las instancias del modelo.
            None: Si ocurre un error.
        """
        session: Session = self.Session()
        try:
            return session.query(model_class).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los {model_class.__name__}: {e}")
            return None
        finally:
            session.close()
