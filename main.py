# main.py - Archivo principal para iniciar la aplicación web de la pizzería con Flet

import flet as ft
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Importa la configuración de la base de datos
from core.config import Config

# Importa el modelo base para la creación de tablas
#from models import Base

# Importa todas las clases de servicios para la interacción con la base de datos
from services.cliente_service import ClienteService
from services.menu_service import MenuService
from services.pedido_service import PedidoService
from services.financiero_service import FinancieroService
from services.pizzeria_info_service import PizzeriaInfoService
from services.administrador_service import AdministradorService

# Importa las vistas de la aplicación
from views.main_view import MainView
from views.admin_view import AdminView

def main(page: ft.Page):
    """
    Función principal de la aplicación Flet.
    Configura la base de datos, los servicios y las rutas de la aplicación.
    """
    # 1. Configuración de la base de datos con SQLAlchemy
    # Crea un motor de base de datos usando la URL de conexión de config.py
    engine = create_engine(Config.DATABASE_URL)
    
    # Crea todas las tablas en la base de datos si no existen.
    # Esto se hace una vez al inicio de la aplicación.
    #Base.metadata.create_all(engine)

    # Crea una fábrica de sesiones, que será utilizada por los servicios.
    Session = sessionmaker(bind=engine)

    # 2. Instanciar todos los servicios
    # Pasa la fábrica de sesiones a cada servicio para que puedan interactuar con la DB.
    cliente_service = ClienteService(Session)
    menu_service = MenuService(Session)
    pedido_service = PedidoService(Session)
    financiero_service = FinancieroService(Session)
    pizzeria_info_service = PizzeriaInfoService(Session)
    administrador_service = AdministradorService(Session)

    # 3. Crear instancias de las vistas
    # La MainView solo necesita la página.
    main_view_instance = MainView(page)
    
    # La AdminView necesita la página y todas las instancias de los servicios
    # para poder gestionar los datos.
    admin_view_instance = AdminView(
        page,
        cliente_service,
        menu_service,
        pedido_service,
        financiero_service,
        pizzeria_info_service,
        administrador_service
    )

    # 4. Gestión de Rutas y Navegación
    def view_pop(view: ft.View):
        """
        Maneja el evento de 'pop' de una vista.
        Elimina la vista superior de la pila y navega a la anterior.
        """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(route_event: ft.RouteChangeEvent):
        """
        Maneja el cambio de ruta de la aplicación.
        Limpia las vistas existentes y añade la vista correspondiente a la nueva ruta.
        """
        page.views.clear() # Limpia la pila de vistas actual

        # Verifica la ruta y añade la vista correspondiente
        if page.route == "/":
            page.views.append(main_view_instance)
        elif page.route == "/admin":
            page.views.append(admin_view_instance)
        # Puedes añadir más rutas y vistas aquí si tu aplicación crece
        
        page.update() # Actualiza la página para mostrar la nueva vista

    # Asigna las funciones de manejo de eventos de navegación a la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inicia la navegación a la ruta actual de la página.
    # Esto asegura que la vista correcta se muestre al inicio de la aplicación.
    page.go(page.route)

# 5. Iniciar la aplicación Flet
# El 'target' especifica la función principal de tu aplicación Flet.
if __name__ == "__main__":
    # ft.app(target=main) # Para ejecutar como una aplicación de escritorio o web simple
    # Para ejecutar como una aplicación web en un navegador, usa view=ft.AppView.WEB_BROWSER
    ft.app(target=main, view=ft.AppView.WEB_BROWSER) # Ejecuta en el navegador
