# services/financiero_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_, func # 'func' ha sido añadido aquí
from datetime import datetime, date, time
from models.models import RegistroFinanciero, Pedido # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService

class FinancieroService(BaseService):
    """
    Servicio para gestionar operaciones CRUD y de búsqueda para el modelo RegistroFinanciero.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    def add_registro(self, monto: float, tipo: str, descripcion: str = None, pedido_id: int = None):
        """
        Añade un nuevo registro financiero (ingreso o gasto).

        Args:
            monto (float): Monto de la transacción.
            tipo (str): 'Ingreso' o 'Gasto'.
            descripcion (str, optional): Descripción del registro. Defaults to None.
            pedido_id (int, optional): ID del pedido si el registro es un ingreso de un pedido. Defaults to None.

        Returns:
            RegistroFinanciero: La instancia del registro financiero añadida.
            None: Si ocurre un error.
        """
        nuevo_registro = RegistroFinanciero(
            monto=monto,
            tipo=tipo,
            descripcion=descripcion,
            pedido_id=pedido_id
        )
        return self.add(nuevo_registro)

    def get_registro_by_id(self, registro_id: int):
        """Obtiene un registro financiero por su ID."""
        return self.get_by_id(RegistroFinanciero, registro_id)

    def update_registro(self, registro_instance: RegistroFinanciero):
        """Actualiza un registro financiero existente."""
        return self.update(registro_instance)

    def delete_registro(self, registro_instance: RegistroFinanciero):
        """Elimina un registro financiero."""
        return self.delete(registro_instance)

    def search_registros_financieros(self, tipo: str = None, fecha_inicio: date = None,
                                     fecha_fin: date = None, pedido_id: int = None):
        """
        Busca registros financieros con varios criterios de filtrado.

        Args:
            tipo (str, optional): 'Ingreso' o 'Gasto' para filtrar. Defaults to None.
            fecha_inicio (date, optional): Fecha de inicio del rango. Defaults to None.
            fecha_fin (date, optional): Fecha de fin del rango. Defaults to None.
            pedido_id (int, optional): ID del pedido para filtrar. Defaults to None.

        Returns:
            list[RegistroFinanciero]: Una lista de registros que coinciden con la búsqueda.
        """
        session: Session = self.Session()
        try:
            q = session.query(RegistroFinanciero)
            if tipo:
                q = q.filter(RegistroFinanciero.tipo.ilike(f'%{tipo}%'))
            if fecha_inicio:
                q = q.filter(RegistroFinanciero.fecha >= datetime.combine(fecha_inicio, time.min))
            if fecha_fin:
                q = q.filter(RegistroFinanciero.fecha <= datetime.combine(fecha_fin, time.max))
            if pedido_id is not None:
                q = q.filter(RegistroFinanciero.pedido_id == pedido_id)
            return q.all()
        except SQLAlchemyError as e:
            print(f"Error al buscar registros financieros: {e}")
            return None
        finally:
            session.close()

    def get_total_ingresos(self, fecha_inicio: date = None, fecha_fin: date = None) -> float:
        """
        Calcula el total de ingresos en un rango de fechas.

        Args:
            fecha_inicio (date, optional): Fecha de inicio. Defaults to None.
            fecha_fin (date, optional): Fecha de fin. Defaults to None.

        Returns:
            float: El total de ingresos.
        """
        session: Session = self.Session()
        try:
            q = session.query(func.sum(RegistroFinanciero.monto)).filter(RegistroFinanciero.tipo == 'Ingreso')
            if fecha_inicio:
                q = q.filter(RegistroFinanciero.fecha >= datetime.combine(fecha_inicio, time.min))
            if fecha_fin:
                q = q.filter(RegistroFinanciero.fecha <= datetime.combine(fecha_fin, time.max))
            total = q.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            print(f"Error al calcular total de ingresos: {e}")
            return 0.0
        finally:
            session.close()

    def get_total_gastos(self, fecha_inicio: date = None, fecha_fin: date = None) -> float:
        """
        Calcula el total de gastos en un rango de fechas.

        Args:
            fecha_inicio (date, optional): Fecha de inicio. Defaults to None.
            fecha_fin (date, optional): Fecha de fin. Defaults to None.

        Returns:
            float: El total de gastos.
        """
        session: Session = self.Session()
        try:
            q = session.query(func.sum(RegistroFinanciero.monto)).filter(RegistroFinanciero.tipo == 'Gasto')
            if fecha_inicio:
                q = q.filter(RegistroFinanciero.fecha >= datetime.combine(fecha_inicio, time.min))
            if fecha_fin:
                q = q.filter(RegistroFinanciero.fecha <= datetime.combine(fecha_fin, time.max))
            total = q.scalar()
            return total if total is not None else 0.0
        except SQLAlchemyError as e:
            print(f"Error al calcular total de gastos: {e}")
            return 0.0
        finally:
            session.close()

    def get_all_registros_financieros(self):
        """Obtiene todos los registros financieros."""
        return self.get_all(RegistroFinanciero)
