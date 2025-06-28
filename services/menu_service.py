# services/menu_service.py
from sqlalchemy.orm import sessionmaker, Session, joinedload # Importar joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from models.models import CategoriaMenu, ItemMenu # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService
import logging # Importa el módulo logging

logger = logging.getLogger(__name__) # Obtiene una instancia del logger para este módulo

class MenuService(BaseService):
    """
    Servicio para gestionar operaciones CRUD y de búsqueda para los modelos
    CategoriaMenu e ItemMenu.
    """
    def __init__(self, Session: sessionmaker):
        super().__init__(Session)

    # --- Métodos para CategoriaMenu ---

    def add_categoria(self, nombre: str, descripcion: str = None):
        """Añade una nueva categoría de menú."""
        try:
            nueva_categoria = CategoriaMenu(nombre=nombre, descripcion=descripcion)
            result = self.add(nueva_categoria)
            logger.info(f"Categoría '{nombre}' añadida con éxito (ID: {result.id if result else 'N/A'}).")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al añadir categoría '{nombre}': {e}")
            return None

    def get_categoria_by_id(self, categoria_id: int):
        """Obtiene una categoría por su ID."""
        try:
            result = self.get_by_id(CategoriaMenu, categoria_id)
            if result:
                logger.debug(f"Categoría encontrada por ID {categoria_id}: {result.nombre}")
            else:
                logger.debug(f"No se encontró categoría con ID {categoria_id}.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener categoría por ID {categoria_id}: {e}")
            return None

    def get_categoria_by_nombre(self, nombre: str):
        """Obtiene una categoría por su nombre."""
        session: Session = self.Session()
        try:
            result = session.query(CategoriaMenu).filter_by(nombre=nombre).first()
            if result:
                logger.debug(f"Categoría encontrada por nombre '{nombre}': {result.id}")
            else:
                logger.debug(f"No se encontró categoría con nombre '{nombre}'.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar categoría por nombre '{nombre}': {e}")
            return None
        finally:
            session.close()

    def update_categoria(self, categoria_instance: CategoriaMenu):
        """Actualiza una categoría existente."""
        try:
            result = self.update(categoria_instance)
            logger.info(f"Categoría '{categoria_instance.nombre}' (ID: {categoria_instance.id}) actualizada con éxito.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar categoría '{categoria_instance.nombre}' (ID: {categoria_instance.id}): {e}")
            return None

    def delete_categoria(self, categoria_instance: CategoriaMenu):
        """Elimina una categoría."""
        try:
            self.delete(categoria_instance)
            logger.info(f"Categoría '{categoria_instance.nombre}' (ID: {categoria_instance.id}) eliminada con éxito.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar categoría '{categoria_instance.nombre}' (ID: {categoria_instance.id}): {e}")
            return False

    def get_all_categorias(self):
        """Obtiene todas las categorías de menú."""
        try:
            result = self.get_all(CategoriaMenu)
            logger.debug(f"Obtenidas {len(result)} categorías.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener todas las categorías: {e}")
            return None

    # --- Métodos para ItemMenu ---

    def add_item_menu(self, nombre: str, precio: float, categoria_id: int,
                      descripcion: str = None, imagen_url: str = None, disponible: bool = True):
        """Añade un nuevo ítem al menú."""
        try:
            nuevo_item = ItemMenu(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                imagen_url=imagen_url,
                disponible=disponible,
                categoria_id=categoria_id
            )
            result = self.add(nuevo_item)
            logger.info(f"Ítem de menú '{nombre}' añadido con éxito (ID: {result.id if result else 'N/A'}).")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al añadir ítem de menú '{nombre}': {e}")
            return None

    def get_item_menu_by_id(self, item_id: int):
        """Obtiene un ítem del menú por su ID."""
        session: Session = self.Session() # Abrir sesión para la consulta
        try:
            # Usar joinedload para cargar la categoría junto con el ítem
            result = session.query(ItemMenu).options(joinedload(ItemMenu.categoria)).filter_by(id=item_id).first()
            if result:
                logger.debug(f"Ítem de menú encontrado por ID {item_id}: {result.nombre}")
            else:
                logger.debug(f"No se encontró ítem de menú con ID {item_id}.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener ítem de menú por ID {item_id}: {e}")
            return None
        finally:
            session.close() # Asegurarse de cerrar la sesión


    def search_items_menu(self, query: str = None, categoria_id: int = None, disponible: bool = None):
        """
        Busca ítems del menú por nombre, descripción, categoría y disponibilidad.

        Args:
            query (str, optional): Término de búsqueda en nombre o descripción. Defaults to None.
            categoria_id (int, optional): ID de la categoría para filtrar. Defaults to None.
            disponible (bool, optional): Filtrar por disponibilidad. Defaults to None.

        Returns:
            list[ItemMenu]: Una lista de ítems del menú que coinciden.
        """
        session: Session = self.Session()
        try:
            q = session.query(ItemMenu).options(joinedload(ItemMenu.categoria)) # Carga ansiosa para categoría
            if query:
                q = q.filter(or_(
                    ItemMenu.nombre.ilike(f'%{query}%'),
                    ItemMenu.descripcion.ilike(f'%{query}%')
                ))
            if categoria_id is not None:
                q = q.filter(ItemMenu.categoria_id == categoria_id)
            if disponible is not None:
                q = q.filter(ItemMenu.disponible == disponible)
            result = q.all()
            logger.debug(f"Búsqueda de ítems del menú para '{query}', categoría {categoria_id}, disponible {disponible}: {len(result)} resultados.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al buscar ítems del menú: {e}")
            return None
        finally:
            session.close()

    def update_item_menu(self, item_instance: ItemMenu):
        """Actualiza un ítem del menú existente."""
        try:
            result = self.update(item_instance)
            logger.info(f"Ítem de menú '{item_instance.nombre}' (ID: {item_instance.id}) actualizado con éxito.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al actualizar ítem de menú '{item_instance.nombre}' (ID: {item_instance.id}): {e}")
            return None

    def delete_item_menu(self, item_instance: ItemMenu):
        """Elimina un ítem del menú."""
        try:
            self.delete(item_instance)
            logger.info(f"Ítem de menú '{item_instance.nombre}' (ID: {item_instance.id}) eliminado con éxito.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al eliminar ítem de menú '{item_instance.nombre}' (ID: {item_instance.id}): {e}")
            return False

    def get_all_items_menu(self):
        """Obtiene todos los ítems del menú, cargando ansiosamente su categoría."""
        session: Session = self.Session() # Abrir sesión para la consulta
        try:
            # Usar joinedload para cargar la categoría junto con el ítem
            result = session.query(ItemMenu).options(joinedload(ItemMenu.categoria)).all()
            logger.debug(f"Obtenidos {len(result)} ítems del menú con categorías cargadas ansiosamente.")
            return result
        except SQLAlchemyError as e:
            logger.error(f"Error al obtener todos los ítems del menú con carga ansiosa: {e}")
            return None
        finally:
            session.close() # Asegurarse de cerrar la sesión
