# services/pedido_service.py
from sqlalchemy.orm import sessionmaker, Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func
from datetime import datetime, date, time
from models.models import Pedido, DetallePedido, Cliente, ItemMenu # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService

class PedidoService(BaseService):
    """
    Servicio para gestionar operaciones CRUD y de búsqueda para los modelos
    Pedido y DetallePedido.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    def add_pedido(self, cliente_id: int, direccion_delivery: str,
                   items_con_cantidad: list[dict], total: float, metodo_pago: str = None):
        """
        Añade un nuevo pedido y sus detalles.

        Args:
            cliente_id (int): ID del cliente que realiza el pedido.
            direccion_delivery (str): Dirección de entrega del pedido.
            items_con_cantidad (list[dict]): Lista de diccionarios,
                                              donde cada dict tiene 'item_id' y 'cantidad'.
                                              Ej: [{'item_id': 1, 'cantidad': 2}, ...].
            total (float): El precio total del pedido.
            metodo_pago (str, optional): El método de pago ('Efectivo', 'Pago Móvil'). Defaults to None.

        Returns:
            Pedido: La instancia del pedido añadido.
            None: Si ocurre un error.
        """
        session: Session = self.Session()
        try:
            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                print(f"Error: Cliente con ID {cliente_id} no encontrado.")
                return None

            # Crea el nuevo pedido
            nuevo_pedido = Pedido(
                cliente_id=cliente.id,
                direccion_delivery=direccion_delivery,
                total=total, # Asigna el total recibido
                metodo_pago=metodo_pago # Asigna el método de pago recibido
            )
            session.add(nuevo_pedido)
            session.flush() # Para obtener el ID del pedido antes de los detalles

            # Añade los detalles del pedido
            for item_data in items_con_cantidad:
                item_menu = session.query(ItemMenu).get(item_data['item_id'])
                if not item_menu:
                    print(f"Advertencia: Ítem de menú con ID {item_data['item_id']} no encontrado. Se omitirá.")
                    continue
                
                detalle = DetallePedido(
                    pedido_id=nuevo_pedido.id,
                    item_menu_id=item_menu.id,
                    cantidad=item_data['cantidad'],
                    precio_unitario=item_menu.precio # Usa el precio actual del ítem del menú
                )
                session.add(detalle)

            session.commit()
            session.refresh(nuevo_pedido)
            return nuevo_pedido
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error al añadir pedido: {e}")
            return None
        finally:
            session.close()

    def get_pedido_by_id(self, pedido_id: int):
        """Obtiene un pedido por su ID, cargando también el cliente y los detalles."""
        session: Session = self.Session()
        try:
            # Cargar el pedido, el cliente asociado y los detalles del pedido
            return session.query(Pedido).options(
                joinedload(Pedido.cliente),
                joinedload(Pedido.detalles).joinedload(DetallePedido.item_menu)
            ).filter_by(id=pedido_id).first()
        except SQLAlchemyError as e:
            print(f"Error al obtener pedido por ID '{pedido_id}': {e}")
            return None
        finally:
            session.close()

    def update_pedido(self, pedido_instance: Pedido):
        """Actualiza un pedido existente."""
        return self.update(pedido_instance)

    def delete_pedido(self, pedido_instance: Pedido):
        """Elimina un pedido y sus detalles asociados."""
        return self.delete(pedido_instance)

    def search_pedidos(self, cliente_id: int = None, estado: str = None,
                       fecha_inicio: date = None, fecha_fin: date = None) -> list[Pedido]:
        """
        Busca pedidos por ID de cliente, estado y/o rango de fechas.

        Args:
            cliente_id (int, optional): ID del cliente. Defaults to None.
            estado (str, optional): Estado del pedido. Defaults to None.
            fecha_inicio (date, optional): Fecha de inicio del rango. Defaults to None.
            fecha_fin (date, optional): Fecha de fin del rango. Defaults to None.

        Returns:
            list[Pedido]: Una lista de pedidos que coinciden con la búsqueda.
        """
        session: Session = self.Session()
        try:
            q = session.query(Pedido).options(joinedload(Pedido.cliente)) # Cargar el cliente para mostrar info
            if cliente_id is not None:
                q = q.filter(Pedido.cliente_id == cliente_id)
            if estado:
                q = q.filter(Pedido.estado.ilike(f'%{estado}%'))
            if fecha_inicio:
                q = q.filter(Pedido.fecha_hora >= datetime.combine(fecha_inicio, time.min))
            if fecha_fin:
                q = q.filter(Pedido.fecha_hora <= datetime.combine(fecha_fin, time.max))
            return q.all()
        except SQLAlchemyError as e:
            print(f"Error al buscar pedidos: {e}")
            return None
        finally:
            session.close()

    def get_all_pedidos(self):
        """Obtiene todos los pedidos, cargando también el cliente asociado."""
        session: Session = self.Session()
        try:
            return session.query(Pedido).options(joinedload(Pedido.cliente)).all()
        except SQLAlchemyError as e:
            print(f"Error al obtener todos los pedidos: {e}")
            return None
        finally:
            session.close()
