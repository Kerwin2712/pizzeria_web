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
            # No cierres la sesión aquí si el objeto va a ser modificado y luego pasado
            # para la actualización en otro método. Es mejor que el método que actualiza
            # sea el responsable de obtener y persistir el objeto.
            return info
        except SQLAlchemyError as e:
            print(f"Error al obtener información de la pizzería: {e}")
            return None
        finally:
            # Aquí es donde usualmente cerrarías la sesión.
            # Sin embargo, para que el objeto retornado esté "desasociado" de la sesión
            # y pueda ser modificado, y luego reasociado, podrías no cerrarla aquí
            # o cargarla en la sesión de actualización.
            session.close() # Mantener el cierre aquí para una lectura simple.

    def update_pizzeria_info_by_data(self, id: int, nombre_pizzeria: str = None, direccion: str = None,
                                     telefono: str = None, email_contacto: str = None,
                                     horario_atencion: str = None, red_social_facebook: str = None,
                                     red_social_instagram: str = None,
                                     pago_movil_banco: str = None, pago_movil_telefono: str = None,
                                     pago_movil_cedula: str = None, pago_movil_cuenta: str = None,
                                     pago_movil_beneficiario: str = None, whatsapp_numero: str = None,
                                     whatsapp_chat_link: str = None):
        """
        Actualiza la información de la pizzería existente basándose en un ID y los nuevos datos.
        Esto asegura que el objeto sea persistente dentro de la sesión de actualización.
        """
        session: Session = self.Session()
        try:
            info = session.query(InformacionPizzeria).filter_by(id=id).first()
            if not info:
                print(f"No se encontró información de la pizzería con ID: {id}")
                return None

            # Actualiza los campos solo si se proporcionan nuevos valores
            if nombre_pizzeria is not None:
                info.nombre_pizzeria = nombre_pizzeria
            if direccion is not None:
                info.direccion = direccion
            if telefono is not None:
                info.telefono = telefono
            if email_contacto is not None:
                info.email_contacto = email_contacto
            if horario_atencion is not None:
                info.horario_atencion = horario_atencion
            if red_social_facebook is not None:
                info.red_social_facebook = red_social_facebook
            if red_social_instagram is not None:
                info.red_social_instagram = red_social_instagram
            
            # Nuevos campos de Pago Móvil
            if pago_movil_banco is not None:
                info.pago_movil_banco = pago_movil_banco
            if pago_movil_telefono is not None:
                info.pago_movil_telefono = pago_movil_telefono
            if pago_movil_cedula is not None:
                info.pago_movil_cedula = pago_movil_cedula
            if pago_movil_cuenta is not None:
                info.pago_movil_cuenta = pago_movil_cuenta
            if pago_movil_beneficiario is not None:
                info.pago_movil_beneficiario = pago_movil_beneficiario
            
            # Nuevos campos de WhatsApp
            if whatsapp_numero is not None:
                info.whatsapp_numero = whatsapp_numero
            if whatsapp_chat_link is not None:
                info.whatsapp_chat_link = whatsapp_chat_link

            session.add(info) # Reasocia el objeto con la sesión (aunque ya esté si fue cargado aquí)
            session.commit()
            session.refresh(info)
            return info
        except SQLAlchemyError as e:
            session.rollback() # Revierte los cambios si hay un error
            print(f"Error al actualizar InformacionPizzeria (ID: {id}): {e}")
            return None
        finally:
            session.close()

    def add_pizzeria_info(self, nombre_pizzeria: str, direccion: str, telefono: str,
                          email_contacto: str = None, horario_atencion: str = None,
                          red_social_facebook: str = None, red_social_instagram: str = None,
                          pago_movil_banco: str = None, pago_movil_telefono: str = None,
                          pago_movil_cedula: str = None, pago_movil_cuenta: str = None,
                          pago_movil_beneficiario: str = None, whatsapp_numero: str = None,
                          whatsapp_chat_link: str = None):
        """
        Añade la información inicial de la pizzería.
        Debería llamarse solo si no existe información previa.
        """
        session: Session = self.Session() # Abre una nueva sesión para esta operación
        try:
            existing_info = session.query(InformacionPizzeria).first()
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
                red_social_instagram=red_social_instagram,
                pago_movil_banco=pago_movil_banco,
                pago_movil_telefono=pago_movil_telefono,
                pago_movil_cedula=pago_movil_cedula,
                pago_movil_cuenta=pago_movil_cuenta,
                pago_movil_beneficiario=pago_movil_beneficiario,
                whatsapp_numero=whatsapp_numero,
                whatsapp_chat_link=whatsapp_chat_link
            )
            session.add(new_info)
            session.commit()
            session.refresh(new_info)
            return new_info
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al añadir información de la pizzería: {e}")
            return None
        finally:
            session.close()


    def delete_pizzeria_info(self, info_instance: InformacionPizzeria):
        """
        Elimina la información de la pizzería. Usar con precaución,
        ya que normalmente solo hay una entrada.
        """
        # Este método también necesitaría manejar la persistencia
        # si info_instance no viene de la sesión actual.
        # Lo ideal sería eliminar por ID.
        session: Session = self.Session()
        try:
            # Reasociar la instancia con la sesión actual
            session.delete(session.merge(info_instance))
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al eliminar InformacionPizzeria: {e}")
            return False
        finally:
            session.close()

