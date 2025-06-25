# main.py - Archivo principal para iniciar la aplicación web de la pizzería con Flet

import flet as ft
import logging # Importa el módulo logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Importa la configuración de la base de datos
from core.config import settings # Importamos la instancia 'settings' directamente

# Importa el modelo base para la creación de tablas
#from core.models import Base

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

# 1. Configuración del Logger
# Define el formato de los mensajes de log
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Configura el logger básico para escribir en un archivo y en la consola
logging.basicConfig(
    level=settings.LOG_LEVEL, # Usa el nivel de log definido en config.py (ej. INFO, DEBUG)
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(settings.LOG_FILE), # Escribe los logs en el archivo especificado en config.py
        logging.StreamHandler() # Muestra los logs también en la consola
    ]
)
# Obtiene una instancia del logger para este módulo
logger = logging.getLogger(__name__)

def main(page: ft.Page):
    """
    Función principal de la aplicación Flet.
    Configura la base de datos, los servicios y las rutas de la aplicación.
    """
    logger.info("Iniciando la aplicación Flet...")

    # 2. Configuración de la base de datos con SQLAlchemy
    try:
        # Crea un motor de base de datos usando la URL de conexión de config.py
        engine = create_engine(settings.DATABASE_URL)
        
        # Crea todas las tablas en la base de datos si no existen.
        #Base.metadata.create_all(engine)
        logger.info("Tablas de la base de datos verificadas/creadas con éxito.")
        
        # Crea una fábrica de sesiones, que será utilizada por los servicios.
        Session = sessionmaker(bind=engine)
        logger.info("Fábrica de sesiones de SQLAlchemy creada.")

    except SQLAlchemyError as e:
        logger.critical(f"Error crítico al conectar o inicializar la base de datos: {e}")
        # En una aplicación real, podrías mostrar un mensaje de error al usuario
        page.add(ft.Text(f"Error crítico de base de datos: {e}. Por favor, contacta a soporte."))
        return # Detiene la ejecución si hay un error crítico de DB

    # 3. Instanciar todos los servicios
    logger.info("Instanciando servicios de la aplicación...")
    cliente_service = ClienteService(Session)
    menu_service = MenuService(Session)
    pedido_service = PedidoService(Session)
    financiero_service = FinancieroService(Session)
    pizzeria_info_service = PizzeriaInfoService(Session)
    administrador_service = AdministradorService(Session)
    logger.info("Servicios instanciados correctamente.")

    # 4. Crear instancias de las vistas
    logger.info("Creando instancias de las vistas...")
    main_view_instance = MainView(page)
    
    admin_view_instance = AdminView(
        page,
        cliente_service,
        menu_service,
        pedido_service,
        financiero_service,
        pizzeria_info_service,
        administrador_service
    )
    logger.info("Vistas creadas correctamente.")

    # 5. Gestión de Rutas y Navegación
    def view_pop(view: ft.View):
        """
        Maneja el evento de 'pop' de una vista.
        Elimina la vista superior de la pila y navega a la anterior.
        """
        logger.info(f"Pop de vista: {view.route}. Volviendo a la vista anterior.")
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    def route_change(route_event: ft.RouteChangeEvent):
        """
        Maneja el cambio de ruta de la aplicación.
        Limpia las vistas existentes y añade la vista correspondiente a la nueva ruta.
        """
        logger.info(f"Cambio de ruta detectado: {route_event.route}")
        page.views.clear() # Limpia la pila de vistas actual

        # Verifica la ruta y añade la vista correspondiente
        if page.route == "/":
            page.views.append(main_view_instance)
            logger.debug("Cargando MainView para la ruta '/'")
        elif page.route == "/admin":
            page.views.append(admin_view_instance)
            logger.debug("Cargando AdminView para la ruta '/admin'")
        else:
            # Manejar rutas no encontradas o redirigir a una página de error
            page.views.append(main_view_instance) # Por defecto, vuelve a la vista principal
            logger.warning(f"Ruta no reconocida: {page.route}. Redirigiendo a la vista principal.")
        
        page.update() # Actualiza la página para mostrar la nueva vista

    # Asigna las funciones de manejo de eventos de navegación a la página
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    # Inicia la navegación a la ruta actual de la página.
    # Esto asegura que la vista correcta se muestre al inicio de la aplicación.
    logger.info(f"Navegando a la ruta inicial: {page.route}")
    page.go(page.route)

# 6. Iniciar la aplicación Flet
if __name__ == "__main__":
    logger.info("Flet app configurada para iniciar.")
    ft.app(target=main, view=settings.FLET_VIEW, port=settings.FLET_PORT)
    logger.info("Flet app iniciada. Puedes acceder a ella a través del navegador.")
