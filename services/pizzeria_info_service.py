# services/pizzeria_info_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from models.models import InformacionPizzeria # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService

class PizzeriaInfoService(BaseService):
    """
    Servicio para gestionar operaciones CRUD (principalmente lectura y actualización)
    para el modelo InformacionPizzeria.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    def get_pizzeria_info(self):
        """
        Obtiene la única instancia de información de la pizzería.
        Si no existe, se puede inicializar.

        Returns:
            InformacionPizzeria: La instancia de información de la pizzería.
            None: Si ocurre un error.
        """
        session: Session = self.Session()
        try:
            info = session.query(InformacionPizzeria).first()
            if not info:
                # Opcional: inicializar con datos por defecto si no existe
                # nuevo_info = InformacionPizzeria(
                #     nombre_pizzeria="Mi Pizzería",
                #     direccion="Dirección por defecto",
                #     telefono="123-456-7890"
                # )
                # session.add(nuevo_info)
                # session.commit()
                # session.refresh(nuevo_info)
                # return nuevo_info
                print("No se encontró información de la pizzería. Por favor, añádela.")
            return info
        except SQLAlchemyError as e:
            print(f"Error al obtener información de la pizzería: {e}")
            return None
        finally:
            session.close()

    def update_pizzeria_info(self, info_instance: InformacionPizzeria):
        """Actualiza la información de la pizzería existente."""
        return self.update(info_instance)

    def add_pizzeria_info(self, nombre_pizzeria: str, direccion: str, telefono: str,
                          email_contacto: str = None, horario_atencion: str = None,
                          red_social_facebook: str = None, red_social_instagram: str = None):
        """
        Añade la información inicial de la pizzería.
        Debería llamarse solo si no existe información previa.
        """
        existing_info = self.get_pizzeria_info()
        if existing_info:
            print("Ya existe información de la pizzería. Usa 'update_pizzeria_info' para modificarla.")
            return existing_info

        new_info = InformacionPizzeria(
            nombre_pizzeria=nombre_pizzeria,
            direccion=direccion,
            telefono=telefono,
            email_contacto=email_contacto,
            horario_atencion=horario_atencion,
            red_social_facebook=red_social_facebook,
            red_social_instagram=red_social_instagram
        )
        return self.add(new_info)

    def delete_pizzeria_info(self, info_instance: InformacionPizzeria):
        """
        Elimina la información de la pizzería. Usar con precaución,
        ya que normalmente solo hay una entrada.
        """
        return self.delete(info_instance)
