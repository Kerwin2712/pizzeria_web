# services/menu_service.py
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from models.models import CategoriaMenu, ItemMenu # Asegúrate que models.py esté en el directorio 'core'
from services.base_service import BaseService

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
        nueva_categoria = CategoriaMenu(nombre=nombre, descripcion=descripcion)
        return self.add(nueva_categoria)

    def get_categoria_by_id(self, categoria_id: int):
        """Obtiene una categoría por su ID."""
        return self.get_by_id(CategoriaMenu, categoria_id)

    def get_categoria_by_nombre(self, nombre: str):
        """Obtiene una categoría por su nombre."""
        session: Session = self.Session()
        try:
            return session.query(CategoriaMenu).filter_by(nombre=nombre).first()
        except SQLAlchemyError as e:
            print(f"Error al buscar categoría por nombre '{nombre}': {e}")
            return None
        finally:
            session.close()

    def update_categoria(self, categoria_instance: CategoriaMenu):
        """Actualiza una categoría existente."""
        return self.update(categoria_instance)

    def delete_categoria(self, categoria_instance: CategoriaMenu):
        """Elimina una categoría."""
        return self.delete(categoria_instance)

    def get_all_categorias(self):
        """Obtiene todas las categorías de menú."""
        return self.get_all(CategoriaMenu)

    # --- Métodos para ItemMenu ---

    def add_item_menu(self, nombre: str, precio: float, categoria_id: int,
                      descripcion: str = None, imagen_url: str = None, disponible: bool = True):
        """Añade un nuevo ítem al menú."""
        nuevo_item = ItemMenu(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            imagen_url=imagen_url,
            disponible=disponible,
            categoria_id=categoria_id
        )
        return self.add(nuevo_item)

    def get_item_menu_by_id(self, item_id: int):
        """Obtiene un ítem del menú por su ID."""
        return self.get_by_id(ItemMenu, item_id)

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
            q = session.query(ItemMenu)
            if query:
                q = q.filter(or_(
                    ItemMenu.nombre.ilike(f'%{query}%'),
                    ItemMenu.descripcion.ilike(f'%{query}%')
                ))
            if categoria_id is not None:
                q = q.filter(ItemMenu.categoria_id == categoria_id)
            if disponible is not None:
                q = q.filter(ItemMenu.disponible == disponible)
            return q.all()
        except SQLAlchemyError as e:
            print(f"Error al buscar ítems del menú: {e}")
            return None
        finally:
            session.close()

    def update_item_menu(self, item_instance: ItemMenu):
        """Actualiza un ítem del menú existente."""
        return self.update(item_instance)

    def delete_item_menu(self, item_instance: ItemMenu):
        """Elimina un ítem del menú."""
        return self.delete(item_instance)

    def get_all_items_menu(self):
        """Obtiene todos los ítems del menú."""
        return self.get_all(ItemMenu)
