# views/admin_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_message_box, create_simple_bar_chart
from datetime import datetime, date
import logging # Importa el módulo logging

# Importaciones de servicios (estos se pasarán al constructor)
from services.cliente_service import ClienteService
from services.menu_service import MenuService
from services.pedido_service import PedidoService
from services.financiero_service import FinancieroService
from services.pizzeria_info_service import PizzeriaInfoService
from services.administrador_service import AdministradorService

logger = logging.getLogger(__name__) # Obtiene una instancia del logger para este módulo

class AdminView(ft.View):
    """
    Vista del panel de administración para gestionar la base de datos de la pizzería.
    Permite a los administradores gestionar menú, clientes, pedidos, finanzas,
    información de la pizzería y otros administradores.
    """
    def __init__(self,
                 page: ft.Page,
                 cliente_service: ClienteService,
                 menu_service: MenuService,
                 pedido_service: PedidoService,
                 financiero_service: FinancieroService,
                 pizzeria_info_service: PizzeriaInfoService,
                 administrador_service: AdministradorService):
        
        super().__init__()
        self.page = page
        self.route = "/admin" # Ruta para esta vista

        # Configuración de colores para modo oscuro (similar a MainView)
        self.page_bg_color = ft.colors.BLACK # Color de fondo general de la vista
        self.card_bg_color = ft.colors.BLUE_GREY_900 # Color de fondo de las tarjetas
        self.text_color = ft.colors.WHITE # Color de texto principal
        self.nav_rail_bg_color = ft.colors.BLUE_GREY_800 # Color de la barra de navegación lateral
        self.appbar_bg_color = ft.colors.BLUE_GREY_900 # Color de la barra superior
        self.textfield_fill_color = ft.colors.BLUE_GREY_700 # Color de fondo de TextField

        # Establece el color de fondo de la VISTA
        self.bgcolor = self.page_bg_color

        # Servicios de base de datos
        self.cliente_service = cliente_service
        self.menu_service = menu_service
        self.pedido_service = pedido_service
        self.financiero_service = financiero_service
        self.pizzeria_info_service = pizzeria_info_service
        self.administrador_service = administrador_service

        # Referencias a los campos de login (para usarlos en el método _admin_login)
        self.admin_username_field = ft.TextField(label="Usuario", hint_text="admin_user", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.admin_password_field = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))

        # Referencias a los campos de información de la pizzería
        self.pizzeria_name_field = ft.TextField(label="Nombre de la Pizzería", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_address_field = ft.TextField(label="Dirección", multiline=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_phone_field = ft.TextField(label="Teléfono", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_email_field = ft.TextField(label="Email de Contacto", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_hours_field = ft.TextField(label="Horario de Atención", multiline=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_facebook_field = ft.TextField(label="URL Facebook", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.pizzeria_instagram_field = ft.TextField(label="URL Instagram", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))

        # Variable para controlar si el administrador está logueado
        self.is_logged_in = False # Por defecto, no logueado. Este estado será actualizado por MainView.

        self.page.title = "Panel de Administración - La Mejor Pizzería"
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.window_height = 800
        self.page.window_width = 1200

        # Contenedor principal para el contenido dinámico de la sección de administración
        self.admin_content_area = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            controls=[]
        )

        # Barra de navegación lateral para el administrador
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True,
            min_width=100,
            min_extended_width=200,
            leading=ft.Container(
                ft.Text("Gestión", size=18, weight=ft.FontWeight.BOLD, color=self.text_color), # Color del texto
                padding=ft.padding.only(top=20, bottom=20, left=10)
            ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label_content=ft.Text("Dashboard", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MENU_BOOK_OUTLINED,
                    selected_icon=ft.icons.MENU_BOOK,
                    label_content=ft.Text("Menú", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINED,
                    selected_icon=ft.icons.PEOPLE,
                    label_content=ft.Text("Clientes", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.RECEIPT_OUTLINED,
                    selected_icon=ft.icons.RECEIPT,
                    label_content=ft.Text("Pedidos", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MONEY_OUTLINED,
                    selected_icon=ft.icons.MONEY,
                    label_content=ft.Text("Finanzas", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BUSINESS_OUTLINED,
                    selected_icon=ft.icons.BUSINESS,
                    label_content=ft.Text("Info Pizzería", color=self.text_color),
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    label_content=ft.Text("Administradores", color=self.text_color),
                ),
            ],
            on_change=self._on_navigation_change,
            bgcolor=self.nav_rail_bg_color, # Color de fondo mejorado
            # border_radius=ft.border_radius.all(10) # No soportado directamente
        )

        # Barra superior para la vista de administrador - ASIGNADA A LA VISTA
        self.appbar = ft.AppBar( # CAMBIO CLAVE: self.page.appbar -> self.appbar
            leading=ft.Icon(ft.icons.SETTINGS, size=30, color=self.text_color),
            leading_width=40,
            title=ft.Text("Panel de Administración", weight=ft.FontWeight.BOLD, color=self.text_color),
            center_title=False,
            bgcolor=self.appbar_bg_color,
            actions=[
                ft.IconButton(ft.icons.LOGOUT, tooltip="Cerrar Sesión", on_click=self._logout, icon_color=self.text_color),
            ],
            toolbar_height=70,
            elevation=4
        )

        # Contenido de la vista
        self.controls = [
            ft.Row(
                [
                    self.navigation_rail,
                    ft.VerticalDivider(width=1, color=ft.colors.BLUE_GREY_700),
                    self.admin_content_area,
                ],
                expand=True,
            )
        ]
        
        # Cargar la sección inicial según el estado de login
        # Ya no se llama a _load_initial_admin_section aquí,
        # la MainView se encargará de establecer is_logged_in y luego cargar el dashboard.
        # No se llama a .update() dentro de esta función ni en las que llama directamente.
        # self._load_initial_admin_section() # Eliminado. La MainView activará la carga del dashboard.

    def _load_initial_admin_section(self):
        """Carga la sección de login o el dashboard si ya está logueado.
           Ahora esta función es llamada externamente por MainView."""
        logger.info("Cargando sección inicial del panel de administración (llamado externo).")
        if self.is_logged_in:
            self._load_dashboard_section()
        else:
            self._load_admin_login_form()
        # El page.update() en main.py o la llamada externa se encargará de esto.

    def _logout(self, e):
        """Cierra la sesión del administrador y regresa a la vista principal."""
        logger.info("Cerrando sesión de administrador.")
        self.is_logged_in = False # Establecer el estado a no logueado
        show_snackbar(self.page, "Sesión de administrador cerrada.", ft.colors.AMBER_700)
        
        # Limpiar campos de login (sin llamar a .update() individualmente)
        self.admin_username_field.value = ""
        self.admin_password_field.value = ""

        # Recargar el formulario de login en AdminView al hacer logout
        self._load_admin_login_form() 
        self.navigation_rail.selected_index = None # Deseleccionar cualquier opción
        
        # Redirige a la ruta principal de la aplicación.
        # Esto automáticamente limpiará la vista actual y cargará la MainView.
        self.page.go("/") 
        self.page.update() # Actualiza la página completa, incluyendo la nueva vista

    def _on_navigation_change(self, e):
        """Maneja el cambio de selección en la barra de navegación lateral del administrador."""
        logger.info(f"Navegación de administrador seleccionada: {e.control.selected_index}")
        # Solo permitir navegación si el administrador está logueado
        if not self.is_logged_in:
            logger.warning("Intento de navegación sin sesión iniciada en AdminView.")
            show_snackbar(self.page, "Por favor, inicia sesión para acceder a las funciones de administración.", ft.colors.RED_500)
            self._load_admin_login_form() # Siempre redirige al formulario de login
            self.navigation_rail.selected_index = None # Deseleccionar cualquier opción
            self.admin_content_area.update() # Mantenemos update aquí, ya que la vista ya debería estar en la página
            self.page.update()
            return

        self.navigation_rail.selected_index = e.control.selected_index
        if self.navigation_rail.selected_index == 0:
            self._load_dashboard_section()
        elif self.navigation_rail.selected_index == 1:
            self._load_menu_management()
        elif self.navigation_rail.selected_index == 2:
            self._load_client_management()
        elif self.navigation_rail.selected_index == 3:
            self._load_order_management()
        elif self.navigation_rail.selected_index == 4:
            self._load_finance_management()
        elif self.navigation_rail.selected_index == 5:
            self._load_pizzeria_info_management()
        elif self.navigation_rail.selected_index == 6:
            self._load_admin_management()
        
        self.admin_content_area.update() # Mantenemos update aquí, ya que la vista ya debería estar en la página
        self.page.update()

    # --- Sección de Login de Administrador ---
    def _load_admin_login_form(self):
        """Carga el formulario de inicio de sesión de administrador."""
        logger.info("Cargando formulario de login de administrador.")
        self.admin_content_area.controls.clear()
        self.admin_content_area.controls.append(
            CustomCard(
                title="⚙️ Acceso de Administrador ⚙️",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Por favor, introduce tus credenciales de administrador.", size=16, color=self.text_color),
                    self.admin_username_field, # Usamos la referencia a los campos
                    self.admin_password_field, # Usamos la referencia a los campos
                    ft.ElevatedButton(
                        "Iniciar Sesión como Administrador",
                        icon=ft.icons.LOGIN,
                        on_click=self._admin_login_from_admin_view # Llama al nuevo método de login para esta vista
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=400
            )
        )
        # Se eliminó la llamada a update aquí porque page.update() en el route_change de main.py
        # es quien finalmente actualiza la vista después de que se añade.
        # self.admin_content_area.update() # Eliminado.

    def _admin_login_from_admin_view(self, e):
        """
        Maneja la lógica de inicio de sesión del administrador cuando se intenta desde AdminView.
        """
        username = self.admin_username_field.value
        password = self.admin_password_field.value

        logger.info(f"Intento de login (desde AdminView) para usuario: {username}")

        if not username or not password:
            show_snackbar(self.page, "Por favor, ingresa usuario y contraseña.", ft.colors.RED_500)
            logger.warning("Intento de login (desde AdminView) fallido: campos vacíos.")
            return

        admin_user = self.administrador_service.get_administrador_by_usuario(username)

        if admin_user and self.administrador_service.check_password(password, admin_user.contrasena_hash):
            self.is_logged_in = True # Marcar como logueado
            logger.info(f"Login exitoso (desde AdminView) para el usuario: {username}")
            show_snackbar(self.page, f"¡Bienvenido, {admin_user.usuario}! Sesión iniciada.", ft.colors.GREEN_500)
            self._load_dashboard_section() # Cargar el dashboard después del login
            self.navigation_rail.selected_index = 0 # Asegurarse de que el dashboard esté seleccionado
        else:
            logger.warning(f"Login (desde AdminView) fallido para el usuario: {username}. Credenciales incorrectas.")
            show_snackbar(self.page, "Usuario o contraseña incorrectos.", ft.colors.RED_500)
        self.admin_content_area.update() # Mantenemos update aquí para el caso de fallo y éxito,
                                         # ya que la vista ya está en la página después del primer render.
        self.page.update()

    # --- Secciones de Gestión (Solo accesibles si is_logged_in es True) ---

    def _load_dashboard_section(self):
        """
        Carga la sección del Dashboard con un resumen rápido.
        """
        logger.info("Cargando sección de Dashboard de administrador.")
        # Solo cargar si está logueado
        if not self.is_logged_in:
            self._load_admin_login_form()
            logger.warning("Intento de acceso a Dashboard sin sesión iniciada.")
            return
        
        self.admin_content_area.controls.clear()

        # Datos de ejemplo o fetched de servicios
        total_clientes = self.cliente_service.get_all_clientes()
        num_clientes = len(total_clientes) if total_clientes else 0

        total_pedidos = self.pedido_service.get_all_pedidos()
        num_pedidos_pendientes = len([p for p in total_pedidos if p.estado == 'Pendiente']) if total_pedidos else 0
        num_pedidos_completados = len([p for p in total_pedidos if p.estado == 'Entregado']) if total_pedidos else 0

        ingresos_hoy = self.financiero_service.get_total_ingresos(date.today(), date.today())
        gastos_hoy = self.financiero_service.get_total_gastos(date.today(), date.today())
        balance_hoy = ingresos_hoy - gastos_hoy

        # Ejemplo de datos para el gráfico (últimos 7 días)
        # Esto sería más dinámico en una app real, calculando ingresos por día
        sales_data = {
            "Lun": 850, "Mar": 920, "Mié": 780, "Jue": 1100, "Vie": 1500, "Sáb": 1800, "Dom": 1600
        }
        
        self.admin_content_area.controls.append(
            ft.Column([
                ft.Text("Dashboard de Administración", size=28, weight=ft.FontWeight.BOLD, color=self.text_color),
                ft.Divider(color=ft.colors.BLUE_GREY_700),
                ft.Row([
                    CustomCard(
                        title="Clientes Registrados",
                        content=ft.Text(str(num_clientes), size=40, weight=ft.FontWeight.BOLD, color=self.text_color),
                        width=250, height=150, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                    CustomCard(
                        title="Pedidos Pendientes",
                        content=ft.Text(str(num_pedidos_pendientes), size=40, weight=ft.FontWeight.BOLD, color=self.text_color),
                        width=250, height=150, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                    CustomCard(
                        title="Ingresos Hoy",
                        content=ft.Text(f"${ingresos_hoy:,.2f}", size=40, weight=ft.FontWeight.BOLD, color=self.text_color),
                        width=250, height=150, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    CustomCard(
                        title="Gastos Hoy",
                        content=ft.Text(f"${gastos_hoy:,.2f}", size=40, weight=ft.FontWeight.BOLD, color=self.text_color),
                        width=250, height=150, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                    CustomCard(
                        title="Balance Hoy",
                        content=ft.Text(f"${balance_hoy:,.2f}", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700 if balance_hoy >= 0 else ft.colors.RED_700),
                        width=200, height=120, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                    CustomCard(
                        title="Pedidos Completados",
                        content=ft.Text(str(num_pedidos_completados), size=40, weight=ft.FontWeight.BOLD, color=self.text_color),
                        width=250, height=150, bgcolor=self.card_bg_color, title_color=self.text_color
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                create_simple_bar_chart(sales_data, "Ventas de la Semana (Ejemplo)", text_color=self.text_color, bar_color=ft.colors.GREEN_400, card_bgcolor=self.card_bg_color, title_color=self.text_color)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        )
        # No self.admin_content_area.update() aquí.

    def _load_menu_management(self):
        """Carga la sección para gestionar el menú (categorías e ítems)."""
        logger.info("Cargando sección de gestión de Menú.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        categories = self.menu_service.get_all_categorias()
        cat_columns = ["ID", "Nombre", "Descripción", "Acciones"] # Añadir columna de acciones
        cat_rows = []
        if categories:
            for cat in categories:
                cat_rows.append([
                    str(cat.id),
                    cat.nombre,
                    cat.descripcion if cat.descripcion else "",
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Editar Categoría",
                            on_click=lambda e, category_id=cat.id: self._open_add_edit_categoria_dialog(e, category_id)
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Eliminar Categoría",
                            on_click=lambda e, category_id=cat.id: self._confirm_delete_categoria(e, category_id)
                        )
                    ])
                ])

        self.admin_content_area.controls.append(
            CustomCard(
                title="🍕 Gestión de Categorías del Menú 📝",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Aquí puedes añadir, editar o eliminar categorías del menú.", size=16, color=self.text_color),
                    create_data_table(cat_columns, cat_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        ft.ElevatedButton("Añadir Categoría", on_click=self._open_add_edit_categoria_dialog),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )

        # --- Gestión de Ítems del Menú ---
        items = self.menu_service.get_all_items_menu()
        item_columns = ["ID", "Nombre", "Precio", "Categoría", "Disponible", "Acciones"] # Añadir columna de acciones
        item_rows = []
        if items:
            for item in items:
                # Obtener el nombre de la categoría
                cat_name = ""
                if item.categoria:
                    cat_name = item.categoria.nombre
                
                item_rows.append([
                    str(item.id),
                    item.nombre,
                    f"${item.precio:,.2f}",
                    cat_name,
                    "Sí" if item.disponible else "No",
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.EDIT,
                            tooltip="Editar Ítem",
                            on_click=lambda e, item_id=item.id: self._open_add_edit_item_dialog(e, item_id)
                        ),
                        ft.IconButton(
                            icon=ft.icons.DELETE,
                            tooltip="Eliminar Ítem",
                            on_click=lambda e, item_id=item.id: self._confirm_delete_item(e, item_id)
                        )
                    ])
                ])

        self.admin_content_area.controls.append(
            CustomCard(
                title="🍔 Gestión de Ítems del Menú 🍟",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Aquí puedes gestionar los ítems específicos de tu menú.", size=16, color=self.text_color),
                    create_data_table(item_columns, item_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        ft.ElevatedButton("Añadir Ítem", on_click=self._open_add_edit_item_dialog),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )
        self.admin_content_area.update()
    
    def _open_add_edit_categoria_dialog(self, e, category_id=None):
        """Abre un diálogo para añadir o editar una categoría."""
        logger.info(f"Abriendo diálogo para {'editar' if category_id else 'añadir'} categoría. ID: {category_id}")
        # Solo cargar si está logueado
        if not self.is_logged_in:
            self._load_admin_login_form()
            return

        is_edit_mode = category_id is not None
        current_category = None
        if is_edit_mode:
            current_category = self.menu_service.get_categoria_by_id(category_id)
            if not current_category:
                show_snackbar(self.page, "Categoría no encontrada.", ft.colors.RED_500)
                logger.warning(f"Intento de editar categoría con ID {category_id} no encontrada.")
                return

        nombre_field = ft.TextField(
            label="Nombre de la Categoría",
            value=current_category.nombre if is_edit_mode else "",
            filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        descripcion_field = ft.TextField(
            label="Descripción (opcional)",
            value=current_category.descripcion if is_edit_mode and current_category.descripcion else "",
            multiline=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )

        def save_categoria(e):
            logger.info(f"Intentando {'actualizar' if is_edit_mode else 'guardar nueva'} categoría.")
            if not nombre_field.value:
                show_snackbar(self.page, "El nombre de la categoría es requerido.", ft.colors.RED_500)
                logger.warning("Fallo al guardar categoría: nombre vacío.")
                return

            if is_edit_mode:
                current_category.nombre = nombre_field.value
                current_category.descripcion = descripcion_field.value
                updated_cat = self.menu_service.update_categoria(current_category)
                if updated_cat:
                    show_snackbar(self.page, f"Categoría '{updated_cat.nombre}' actualizada con éxito.", ft.colors.GREEN_500)
                    logger.info(f"Categoría '{updated_cat.nombre}' actualizada con éxito (ID: {updated_cat.id}).")
                else:
                    show_snackbar(self.page, "Error al actualizar la categoría.", ft.colors.RED_500)
                    logger.error(f"Error al actualizar la categoría con ID {category_id}.")
            else:
                new_cat = self.menu_service.add_categoria(nombre_field.value, descripcion_field.value)
                if new_cat:
                    show_snackbar(self.page, f"Categoría '{new_cat.nombre}' añadida con éxito.", ft.colors.GREEN_500)
                    logger.info(f"Categoría '{new_cat.nombre}' añadida con éxito (ID: {new_cat.id}).")
                else:
                    show_snackbar(self.page, "Error al añadir la categoría.", ft.colors.RED_500)
                    logger.error("Error al añadir la categoría.")
            
            self.page.close(dialog) # Cierra el diálogo
            self._load_menu_management() # Recarga la sección para mostrar los cambios

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{'Editar' if is_edit_mode else 'Añadir Nueva'} Categoría", color=self.text_color),
            content=ft.Column([
                nombre_field,
                descripcion_field
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton("Guardar", on_click=save_categoria)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.card_bg_color, # Fondo del diálogo
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.open(dialog)
        dialog.open = True
        self.page.update()

    def _confirm_delete_categoria(self, e, category_id: int):
        """Muestra un diálogo de confirmación antes de eliminar una categoría."""
        logger.info(f"Confirmación de eliminación para categoría ID: {category_id}.")
        # Solo cargar si está logueado
        if not self.is_logged_in:
            self._load_admin_login_form()
            return

        category_to_delete = self.menu_service.get_categoria_by_id(category_id)
        if not category_to_delete:
            show_snackbar(self.page, "Categoría no encontrada para eliminar.", ft.colors.RED_500)
            logger.warning(f"Intento de eliminar categoría con ID {category_id} no encontrada.")
            return

        def delete_confirmed(e):
            logger.info(f"Eliminando categoría ID: {category_id}.")
            result = self.menu_service.delete_categoria(category_to_delete)
            if result:
                show_snackbar(self.page, f"Categoría '{category_to_delete.nombre}' eliminada con éxito.", ft.colors.GREEN_500)
                logger.info(f"Categoría '{category_to_delete.nombre}' eliminada con éxito (ID: {category_to_delete.id}).")
                self._load_menu_management() # Recarga la sección para mostrar los cambios
            else:
                show_snackbar(self.page, "Error al eliminar la categoría.", ft.colors.RED_500)
                logger.error(f"Error al eliminar la categoría con ID {category_id}.")
            self.page.close(confirm_dialog) # Cierra el diálogo

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación", color=self.text_color),
            content=ft.Text(f"¿Estás seguro de que quieres eliminar la categoría '{category_to_delete.nombre}'? Esta acción no se puede deshacer.", color=self.text_color),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(confirm_dialog)),
                ft.ElevatedButton("Eliminar", on_click=delete_confirmed, style=ft.ButtonStyle(bgcolor=ft.colors.RED_700)) # CAMBIO AQUI
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.card_bg_color,
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.open(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()

    def _open_add_edit_item_dialog(self, e, item_id=None):
        """Abre un diálogo para añadir o editar un ítem del menú."""
        logger.info(f"Abriendo diálogo para {'editar' if item_id else 'añadir'} ítem del menú. ID: {item_id}")
        # Solo cargar si está logueado
        if not self.is_logged_in:
            self._load_admin_login_form()
            return

        is_edit_mode = item_id is not None
        current_item = None
        if is_edit_mode:
            current_item = self.menu_service.get_item_menu_by_id(item_id)
            if not current_item:
                show_snackbar(self.page, "Ítem del menú no encontrado.", ft.colors.RED_500)
                logger.warning(f"Intento de editar ítem con ID {item_id} no encontrado.")
                return

        nombre_field = ft.TextField(
            label="Nombre del Ítem",
            value=current_item.nombre if is_edit_mode else "",
            filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        descripcion_field = ft.TextField(
            label="Descripción (opcional)",
            value=current_item.descripcion if is_edit_mode and current_item.descripcion else "",
            multiline=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        precio_field = ft.TextField(
            label="Precio",
            value=str(current_item.precio) if is_edit_mode else "",
            keyboard_type=ft.KeyboardType.NUMBER, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        imagen_url_field = ft.TextField(
            label="URL de Imagen (opcional)",
            value=current_item.imagen_url if is_edit_mode and current_item.imagen_url else "",
            filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        disponible_checkbox = ft.Checkbox(
            label="Disponible",
            value=current_item.disponible if is_edit_mode else True,
            check_color=ft.colors.WHITE, fill_color=ft.colors.BLUE_GREY_700, label_style=ft.TextStyle(color=self.text_color)
        )

        categorias = self.menu_service.get_all_categorias()
        categoria_dropdown_options = [ft.dropdown.Option(str(c.id), c.nombre) for c in categorias]
        
        initial_category_value = str(current_item.categoria_id) if is_edit_mode else None
        categoria_dropdown = ft.Dropdown(
            label="Categoría",
            options=categoria_dropdown_options,
            value=initial_category_value,
            filled=True,
            fill_color=self.textfield_fill_color,
            color=self.text_color,
            label_style=ft.TextStyle(color=ft.colors.WHITE54),
            hint_style=ft.TextStyle(color=ft.colors.WHITE54),
            text_style=ft.TextStyle(color=self.text_color)
        )

        def save_item(e):
            logger.info(f"Intentando {'actualizar' if is_edit_mode else 'guardar nuevo'} ítem del menú.")
            try:
                precio = float(precio_field.value)
            except ValueError:
                show_snackbar(self.page, "El precio debe ser un número válido.", ft.colors.RED_500)
                logger.warning("Fallo al guardar ítem: precio inválido.")
                return

            if not nombre_field.value or not categoria_dropdown.value:
                show_snackbar(self.page, "Nombre y Categoría son requeridos.", ft.colors.RED_500)
                logger.warning("Fallo al guardar ítem: nombre o categoría vacíos.")
                return

            if is_edit_mode:
                current_item.nombre = nombre_field.value
                current_item.descripcion = descripcion_field.value
                current_item.precio = precio
                current_item.imagen_url = imagen_url_field.value
                current_item.disponible = disponible_checkbox.value
                current_item.categoria_id = int(categoria_dropdown.value)
                updated_item = self.menu_service.update_item_menu(current_item)
                if updated_item:
                    show_snackbar(self.page, f"Ítem '{updated_item.nombre}' actualizado con éxito.", ft.colors.GREEN_500)
                    logger.info(f"Ítem '{updated_item.nombre}' actualizado con éxito (ID: {updated_item.id}).")
                else:
                    show_snackbar(self.page, "Error al actualizar el ítem.", ft.colors.RED_500)
                    logger.error(f"Error al actualizar el ítem con ID {item_id}.")
            else:
                new_item = self.menu_service.add_item_menu(
                    nombre=nombre_field.value,
                    descripcion=descripcion_field.value,
                    precio=precio,
                    categoria_id=int(categoria_dropdown.value),
                    imagen_url=imagen_url_field.value,
                    disponible=disponible_checkbox.value
                )
                if new_item:
                    show_snackbar(self.page, f"Ítem '{new_item.nombre}' añadido con éxito.", ft.colors.GREEN_500)
                    logger.info(f"Ítem '{new_item.nombre}' añadido con éxito (ID: {new_item.id}).")
                else:
                    show_snackbar(self.page, "Error al añadir el ítem.", ft.colors.RED_500)
                    logger.error("Error al añadir el ítem del menú.")
            
            self.page.close(dialog)
            self._load_menu_management()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"{'Editar' if is_edit_mode else 'Añadir Nuevo'} Ítem al Menú", color=self.text_color),
            content=ft.Column([
                nombre_field,
                descripcion_field,
                precio_field,
                imagen_url_field,
                disponible_checkbox,
                categoria_dropdown
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(dialog)),
                ft.ElevatedButton("Guardar", on_click=save_item)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.card_bg_color, # Fondo del diálogo
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.open(dialog)
        dialog.open = True
        self.page.update()

    def _confirm_delete_item(self, e, item_id: int):
        """Muestra un diálogo de confirmación antes de eliminar un ítem del menú."""
        logger.info(f"Confirmación de eliminación para ítem ID: {item_id}.")
        # Solo cargar si está logueado
        if not self.is_logged_in:
            self._load_admin_login_form()
            return

        item_to_delete = self.menu_service.get_item_menu_by_id(item_id)
        if not item_to_delete:
            show_snackbar(self.page, "Ítem del menú no encontrado para eliminar.", ft.colors.RED_500)
            logger.warning(f"Intento de eliminar ítem con ID {item_id} no encontrado.")
            return

        def delete_confirmed(e):
            logger.info(f"Eliminando ítem ID: {item_id}.")
            result = self.menu_service.delete_item_menu(item_to_delete)
            if result:
                show_snackbar(self.page, f"Ítem '{item_to_delete.nombre}' eliminado con éxito.", ft.colors.GREEN_500)
                logger.info(f"Ítem '{item_to_delete.nombre}' eliminado con éxito (ID: {item_to_delete.id}).")
                self._load_menu_management() # Recarga la sección para mostrar los cambios
            else:
                show_snackbar(self.page, "Error al eliminar el ítem.", ft.colors.RED_500)
                logger.error(f"Error al eliminar el ítem con ID {item_id}.")
            self.page.close(confirm_dialog) # Cierra el diálogo

        confirm_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Eliminación", color=self.text_color),
            content=ft.Text(f"¿Estás seguro de que quieres eliminar el ítem '{item_to_delete.nombre}'? Esta acción no se puede deshacer.", color=self.text_color),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(confirm_dialog)),
                ft.ElevatedButton("Eliminar", on_click=delete_confirmed, style=ft.ButtonStyle(bgcolor=ft.colors.RED_700)) # CAMBIO AQUÍ: Eliminado ft.MaterialState.DEFAULT
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.card_bg_color,
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.open(confirm_dialog)
        confirm_dialog.open = True
        self.page.update()

    def _load_client_management(self):
        """Carga la sección para gestionar clientes."""
        logger.info("Cargando sección de gestión de Clientes.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        clientes = self.cliente_service.get_all_clientes()
        client_columns = ["ID", "Nombre", "Email", "Teléfono", "Dirección", "Registro"]
        client_rows = []
        if clientes:
            for client in clientes:
                reg_date = client.fecha_registro.strftime("%Y-%m-%d %H:%M") if client.fecha_registro else "N/A"
                client_rows.append([
                    str(client.id), client.nombre, client.email,
                    client.telefono if client.telefono else "N/A",
                    client.direccion, reg_date
                ])

        self.admin_content_area.controls.append(
            CustomCard(
                title="👥 Gestión de Clientes 👥",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Gestiona los clientes registrados en tu pizzería.", size=16, color=self.text_color),
                    create_data_table(client_columns, client_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Cliente", on_click=lambda e: show_snackbar(self.page, "Añadir cliente - implementar.")),
                        # ft.ElevatedButton("Editar Cliente", on_click=lambda e: show_snackbar(self.page, "Editar cliente - implementar.")),
                        # ft.ElevatedButton("Eliminar Cliente", on_click=lambda e: show_snackbar(self.page, "Eliminar cliente - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )
        self.admin_content_area.update()

    def _load_order_management(self):
        """Carga la sección para gestionar pedidos."""
        logger.info("Cargando sección de gestión de Pedidos.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        pedidos = self.pedido_service.get_all_pedidos()
        order_columns = ["ID", "Cliente", "Fecha/Hora", "Total", "Estado", "Dirección"]
        order_rows = []
        if pedidos:
            for order in pedidos:
                client_name = order.cliente.nombre if order.cliente else "Desconocido"
                order_date_time = order.fecha_hora.strftime("%Y-%m-%d %H:%M") if order.fecha_hora else "N/A"
                order_rows.append([
                    str(order.id), client_name, order_date_time,
                    f"${order.total:,.2f}", order.estado, order.direccion_delivery
                ])

        self.admin_content_area.controls.append(
            CustomCard(
                title="📋 Gestión de Pedidos 📋",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Monitorea y gestiona el estado de todos los pedidos.", size=16, color=self.text_color),
                    create_data_table(order_columns, order_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        # ft.ElevatedButton("Ver Detalles", on_click=lambda e: show_snackbar(self.page, "Ver detalles de pedido - implementar.")),
                        # ft.ElevatedButton("Actualizar Estado", on_click=lambda e: show_snackbar(self.page, "Actualizar estado de pedido - implementar.")),
                        # ft.ElevatedButton("Eliminar Pedido", on_click=lambda e: show_snackbar(self.page, "Eliminar pedido - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )
        self.admin_content_area.update()

    def _load_finance_management(self):
        """Carga la sección para gestionar las finanzas (ingresos/gastos)."""
        logger.info("Cargando sección de gestión de Finanzas.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        registros = self.financiero_service.get_all_registros_financieros()
        finance_columns = ["ID", "Fecha", "Tipo", "Monto", "Descripción", "Pedido ID"]
        finance_rows = []
        if registros:
            for rec in registros:
                rec_date = rec.fecha.strftime("%Y-%m-%d %H:%M") if rec.fecha else "N/A"
                finance_rows.append([
                    str(rec.id), rec_date, rec.tipo, f"${rec.monto:,.2f}",
                    rec.descripcion if rec.descripcion else "", str(rec.pedido_id) if rec.pedido_id else "N/A"
                ])
        
        # Calcular totales (ejemplo para el mes actual)
        today = date.today()
        first_day_of_month = date(today.year, today.month, 1)
        # Esto es una simplificación, para un mes exacto se podría usar:
        # import calendar
        # _, last_day = calendar.monthrange(today.year, today.month)
        # last_day = date(today.year, today.month, last_day)
        last_day_of_month = date(today.year, today.month, 28) # Simplificado, mejor usar calendar.monthrange
        
        total_ingresos_mes = self.financiero_service.get_total_ingresos(first_day_of_month, last_day_of_month)
        total_gastos_mes = self.financiero_service.get_total_gastos(first_day_of_month, last_day_of_month)
        balance_mes = total_ingresos_mes - total_gastos_mes


        self.admin_content_area.controls.append(
            CustomCard(
                title="💰 Gestión de Finanzas 📊",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Registros de ingresos y gastos de la pizzería.", size=16, color=self.text_color),
                    ft.Row([
                        CustomCard(
                            title=f"Ingresos {today.strftime('%B')}",
                            content=ft.Text(f"${total_ingresos_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD, color=self.text_color),
                            width=200, height=120, bgcolor=self.card_bg_color, title_color=self.text_color
                        ),
                        CustomCard(
                            title=f"Gastos {today.strftime('%B')}",
                            content=ft.Text(f"${total_gastos_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD, color=self.text_color),
                            width=200, height=120, bgcolor=self.card_bg_color, title_color=self.text_color
                        ),
                        CustomCard(
                            title=f"Balance {today.strftime('%B')}",
                            content=ft.Text(f"${balance_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700 if balance_mes >= 0 else ft.colors.RED_700),
                            width=200, height=120, bgcolor=self.card_bg_color, title_color=self.text_color
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(color=ft.colors.BLUE_GREY_700),
                    create_data_table(finance_columns, finance_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Registro", on_click=lambda e: show_snackbar(self.page, "Añadir registro financiero - implementar.")),
                        # ft.ElevatedButton("Editar Registro", on_click=lambda e: show_snackbar(self.page, "Editar registro financiero - implementar.")),
                        # ft.ElevatedButton("Eliminar Registro", on_click=lambda e: show_snackbar(self.page, "Eliminar registro financiero - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )
        self.admin_content_area.update()

    def _load_pizzeria_info_management(self):
        """Carga la sección para gestionar la información de la pizzería."""
        logger.info("Cargando sección de gestión de Información de Pizzería.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        info = self.pizzeria_info_service.get_pizzeria_info()
        
        # Asigna los valores actuales de la información de la pizzería a los campos de texto
        self.pizzeria_name_field.value = info.nombre_pizzeria if info else ""
        self.pizzeria_address_field.value = info.direccion if info else ""
        self.pizzeria_phone_field.value = info.telefono if info else ""
        self.pizzeria_email_field.value = info.email_contacto if info else ""
        self.pizzeria_hours_field.value = info.horario_atencion if info else ""
        self.pizzeria_facebook_field.value = info.red_social_facebook if info else ""
        self.pizzeria_instagram_field.value = info.red_social_instagram if info else ""

        self.admin_content_area.controls.append(
            CustomCard(
                title="🏢 Gestión de Información de la Pizzería 📋",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    self.pizzeria_name_field,
                    self.pizzeria_address_field,
                    self.pizzeria_phone_field,
                    self.pizzeria_email_field,
                    self.pizzeria_hours_field,
                    self.pizzeria_facebook_field,
                    self.pizzeria_instagram_field,
                    ft.ElevatedButton("Guardar Cambios", on_click=self._save_pizzeria_info) # Nuevo método para guardar
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15),
                width=600
            )
        )
        # No self.admin_content_area.update() aquí.

    def _save_pizzeria_info(self, e):
        """Método para guardar la información de la pizzería."""
        logger.info("Intentando guardar información de la pizzería.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return

        # Acceder a los valores directamente desde los atributos de la instancia
        nombre_pizzeria = self.pizzeria_name_field.value
        direccion = self.pizzeria_address_field.value
        telefono = self.pizzeria_phone_field.value
        email_contacto = self.pizzeria_email_field.value
        horario_atencion = self.pizzeria_hours_field.value
        red_social_facebook = self.pizzeria_facebook_field.value
        red_social_instagram = self.pizzeria_instagram_field.value

        if not nombre_pizzeria or not direccion or not telefono:
            show_snackbar(self.page, "Nombre, Dirección y Teléfono son requeridos.", ft.colors.RED_500)
            logger.warning("Fallo al guardar información de pizzería: campos requeridos vacíos.")
            return

        # Vuelve a obtener la instancia info dentro de la misma sesión para asegurar persistencia.
        info = self.pizzeria_info_service.get_pizzeria_info()

        if info: # Si ya existe, actualiza
            # Usar el nuevo método update_pizzeria_info_by_data
            updated_info = self.pizzeria_info_service.update_pizzeria_info_by_data(
                id=info.id, # Pasa el ID del objeto existente
                nombre_pizzeria=nombre_pizzeria,
                direccion=direccion,
                telefono=telefono,
                email_contacto=email_contacto,
                horario_atencion=horario_atencion,
                red_social_facebook=red_social_facebook,
                red_social_instagram=red_social_instagram
            )
            if updated_info:
                show_snackbar(self.page, "Información de la pizzería actualizada con éxito.", ft.colors.GREEN_500)
                logger.info("Información de la pizzería actualizada con éxito.")
                # Actualizar el nombre de la pizzería en la MainView si está visible
                # Esto requerirá una forma de comunicar el cambio a MainView, por ahora se quedará con el nombre inicial
                # o se requerirá recargar la MainView. Para simplificar, Flet actualizará el texto la próxima vez que se cargue la vista.
            else:
                show_snackbar(self.page, "Error al actualizar la información.", ft.colors.RED_500)
                logger.error("Error al actualizar la información de la pizzería.")
        else: # Si no existe, añade una nueva
            new_info = self.pizzeria_info_service.add_pizzeria_info(
                nombre_pizzeria=nombre_pizzeria,
                direccion=direccion,
                telefono=telefono,
                email_contacto=email_contacto,
                horario_atencion=horario_atencion,
                red_social_facebook=red_social_facebook,
                red_social_instagram=red_social_instagram
            )
            if new_info:
                show_snackbar(self.page, "Información de la pizzería añadida con éxito.", ft.colors.GREEN_500)
                logger.info("Información de la pizzería añadida con éxito (primera vez).")
                # Recargar la sección para que los campos se muestren con los nuevos valores
                self._load_pizzeria_info_management()
            else:
                show_snackbar(self.page, "Error al añadir la información inicial.", ft.colors.RED_500)
                logger.error("Error al añadir la información inicial de la pizzería.")
        self.page.update()

    def _load_admin_management(self):
        """Carga la sección para gestionar otros administradores (solo para super-admins)."""
        logger.info("Cargando sección de gestión de Administradores.")
        if not self.is_logged_in:
            self._load_admin_login_form()
            return
        self.admin_content_area.controls.clear()
        
        admins = self.administrador_service.get_all_administradores()
        admin_columns = ["ID", "Usuario", "Email", "Super Admin"]
        admin_rows = []
        if admins:
            for admin in admins:
                admin_rows.append([str(admin.id), admin.usuario, admin.email if admin.email else "N/A", "Sí" if admin.super_admin else "No"])

        self.admin_content_area.controls.append(
            CustomCard(
                title="⚙️ Gestión de Administradores 👤",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Administra las cuentas con acceso al panel de control.", size=16, color=self.text_color),
                    create_data_table(admin_columns, admin_rows,
                                      heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                                      data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                                      border_color=ft.colors.BLUE_GREY_700,
                                      text_color=self.text_color),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Admin", on_click=lambda e: show_snackbar(self.page, "Añadir admin - implementar.")),
                        # ft.ElevatedButton("Editar Admin", on_click=lambda e: show_snackbar(self.page, "Editar admin - implementar.")),
                        # ft.ElevatedButton("Eliminar Admin", on_click=lambda e: show_snackbar(self.page, "Eliminar admin - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )
        self.admin_content_area.update()
