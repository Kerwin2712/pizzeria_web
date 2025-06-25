# views/main_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_date_picker, create_time_picker, create_message_box, create_simple_bar_chart
import logging # Importa el módulo logging

# Importamos el servicio de administrador
from services.administrador_service import AdministradorService
from views.admin_view import AdminView # Importa AdminView para poder manipular su instancia

logger = logging.getLogger(__name__) # Obtiene una instancia del logger para este módulo

class MainView(ft.View):
    """
    Vista principal de la aplicación de la pizzería.
    Contiene la barra de navegación lateral, la barra superior y el contenido dinámico.
    """
    def __init__(self, page: ft.Page, administrador_service: AdministradorService, admin_view_instance: AdminView): # Recibe el servicio y la instancia de AdminView
        super().__init__()
        self.page = page
        self.route = "/" # Ruta por defecto para esta vista

        # Instancia del servicio de administrador
        self.administrador_service = administrador_service
        # Instancia de AdminView para poder manipular su estado
        self.admin_view_instance = admin_view_instance

        # Referencias a los campos de texto para el login
        self.admin_username_field = ft.TextField(
            label="Usuario",
            hint_text="admin_user",
            filled=True,
            fill_color=ft.colors.BLUE_GREY_800, # Ajusta a tu preferencia
            color=ft.colors.WHITE,
            hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )
        self.admin_password_field = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            filled=True,
            fill_color=ft.colors.BLUE_GREY_800, # Ajusta a tu preferencia
            color=ft.colors.WHITE,
            hint_style=ft.TextStyle(color=ft.colors.WHITE54)
        )

        # Configuración de colores para modo oscuro
        self.page_bg_color = ft.colors.BLACK # Color de fondo general de la página/vista
        self.card_bg_color = ft.colors.BLUE_GREY_900 # Color de fondo de las tarjetas
        self.text_color = ft.colors.WHITE # Color de texto principal
        self.nav_rail_bg_color = ft.colors.BLUE_GREY_900 # Color de fondo de la barra de navegación lateral
        self.textfield_fill_color = ft.colors.BLUE_GREY_800 # Color de fondo para los TextField

        self.drawer_open = False # Estado del drawer (panel lateral)

        # Define el NavRail y su contenido
        self.navigation_rail = self._create_navigation_rail()

        # Define el área de contenido principal
        self.main_content_area = ft.Column(
            [
                ft.Text("Bienvenido al Sistema de Gestión de Pizzería!", size=24, weight=ft.FontWeight.BOLD, color=self.text_color),
                ft.Text("Selecciona una opción del menú lateral.", size=16, color=self.text_color),
            ],
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO # Permite scroll si el contenido es grande
        )

        # Define el layout general de la vista
        self.controls = [
            ft.Row(
                [
                    self.navigation_rail,
                    ft.VerticalDivider(width=1),
                    self.main_content_area,
                ],
                expand=True,
            )
        ]

    def _create_navigation_rail(self):
        """Crea la barra de navegación lateral."""
        return ft.NavigationRail(
            selected_index=0, # Índice seleccionado inicialmente
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True, # Inicia extendido
            min_width=100,
            min_extended_width=200,
            bgcolor=self.nav_rail_bg_color,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME,
                    label="Inicio",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.LOCAL_PIZZA_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.LOCAL_PIZZA),
                    label="Menú",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SHOPPING_CART_OUTLINED,
                    selected_icon=ft.icons.SHOPPING_CART,
                    label="Pedidos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINED,
                    selected_icon=ft.icons.PEOPLE,
                    label="Clientes",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    label="Administrador",
                ),
            ],
            on_change=self._on_navigation_rail_change,
        )

    def _on_navigation_rail_change(self, e: ft.ControlEvent):
        """Maneja el cambio de selección en el NavRail."""
        logger.info(f"Navegación seleccionada: {e.control.selected_index}")
        if e.control.selected_index == 0:
            self._load_home_section()
        elif e.control.selected_index == 1:
            show_snackbar(self.page, "Sección de Menú - ¡Implementar!")
            self._load_menu_section() # Puedes definir esta función
        elif e.control.selected_index == 2:
            show_snackbar(self.page, "Sección de Pedidos - ¡Implementar!")
            self._load_orders_section() # Puedes definir esta función
        elif e.control.selected_index == 3:
            show_snackbar(self.page, "Sección de Clientes - ¡Implementar!")
            self._load_customers_section() # Puedes definir esta función
        elif e.control.selected_index == 4:
            self._load_admin_section()
        self.page.update()

    def _load_home_section(self):
        """Carga la sección de inicio."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="🍕 ¡Bienvenido a la Pizzería Acme! 🍕",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column(
                    [
                        ft.Text("Explora nuestro delicioso menú o gestiona tu pedido.", size=16, color=self.text_color),
                        ft.Text("¡Tu destino favorito para las mejores pizzas!", size=16, color=self.text_color),
                        ft.ElevatedButton("Ver Menú", on_click=lambda e: self._on_navigation_rail_change(ft.ControlEvent(selected_index=1, control=self.navigation_rail))),
                        ft.Divider(color=ft.colors.BLUE_GREY_700),
                        ft.Text("Oferta del Día:", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
                        ft.Text("¡Pizza Grande de Pepperoni con un 20% de descuento!", size=16, color=ft.colors.RED_500),
                        ft.Image(
                            src="https://placehold.co/400x200/FF5733/FFFFFF?text=Pizza+Oferta",
                            width=400,
                            height=200,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(10)
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        self.main_content_area.update() # Asegura que la UI se actualice

    def _load_menu_section(self):
        """Carga la sección del menú."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="📜 Nuestro Delicioso Menú 📜",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Aquí puedes encontrar todas nuestras opciones de pizzas, bebidas y postres.", size=16, color=self.text_color),
                    ft.Text("¡Pronto podrás ver los ítems de tu base de datos aquí!", size=14, color=ft.colors.WHITE54),
                    # Tabla de datos simulada o con datos reales si se integra el servicio
                    create_data_table(
                        ["Ítem", "Descripción", "Precio"],
                        [
                            ["Pizza Margherita", "Tomate, mozzarella, albahaca fresca", "$10.00"],
                            ["Pizza Pepperoni", "Pepperoni, mozzarella, salsa de tomate", "$12.00"],
                            ["Refresco Grande", "Varios sabores", "$3.50"],
                        ],
                        heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                        data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                        border_color=ft.colors.BLUE_GREY_700,
                        text_color=self.text_color
                    ),
                    ft.ElevatedButton("Hacer Pedido", on_click=lambda e: self._on_navigation_rail_change(ft.ControlEvent(selected_index=2, control=self.navigation_rail))),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )
        self.main_content_area.update()

    def _load_orders_section(self):
        """Carga la sección de pedidos."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="🛒 Realiza tu Pedido 🛒",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Completa los detalles para tu pedido y dirección de envío.", size=16, color=self.text_color),
                    ft.TextField(label="Nombre Completo", hint_text="Juan Pérez", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)),
                    ft.TextField(label="Dirección de Envío", hint_text="Calle Falsa 123, Springfield", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)),
                    ft.TextField(label="Teléfono", hint_text="04XX-XXXXXXX", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)),
                    ft.ElevatedButton(
                        "Confirmar Pedido",
                        icon=ft.icons.CHECK_CIRCLE,
                        on_click=lambda e: show_snackbar(self.page, "¡Pedido simulado realizado con éxito!", ft.colors.GREEN_700)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15),
                width=600
            )
        )
        self.main_content_area.update()

    def _load_customers_section(self):
        """Carga la sección de clientes."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="👥 Gestión de Clientes (Simulado) 👥",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Aquí se mostraría la información de tus clientes.", size=16, color=self.text_color),
                    ft.Text("Esta sección aún no está conectada a la base de datos de clientes.", size=14, color=ft.colors.WHITE54),
                    create_data_table(
                        ["ID", "Nombre", "Email", "Teléfono"],
                        [
                            ["1", "Ana García", "ana@example.com", "555-1234"],
                            ["2", "Luis Martínez", "luis@example.com", "555-5678"],
                        ],
                        heading_row_bgcolor=ft.colors.BLUE_GREY_700,
                        data_row_bgcolor_hover=ft.colors.BLUE_GREY_800,
                        border_color=ft.colors.BLUE_GREY_700,
                        text_color=self.text_color
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )
        self.main_content_area.update()

    def _load_admin_section(self):
        """Carga la sección de acceso de administrador."""
        logger.info("Cargando sección de acceso de administrador.")
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
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
                        on_click=self._admin_login # Llama al nuevo método de login
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=400
            )
        )
        self.main_content_area.update() # Asegura que la UI se actualice

    def _admin_login(self, e):
        """
        Maneja la lógica de inicio de sesión del administrador.
        """
        username = self.admin_username_field.value
        password = self.admin_password_field.value

        logger.info(f"Intento de login para usuario: {username}")

        if not username or not password:
            show_snackbar(self.page, "Por favor, ingresa usuario y contraseña.", ft.colors.RED_500)
            logger.warning("Intento de login fallido: campos vacíos.")
            return

        admin_user = self.administrador_service.get_administrador_by_usuario(username)

        if admin_user and self.administrador_service.check_password(password, admin_user.contrasena_hash):
            logger.info(f"Login exitoso para el usuario: {username}")
            show_snackbar(self.page, f"¡Bienvenido, {admin_user.usuario}! Sesión iniciada.", ft.colors.GREEN_500)
            
            # Establecer el estado de login en la instancia de AdminView
            self.admin_view_instance.is_logged_in = True
            # Forzar la recarga del dashboard en AdminView
            self.admin_view_instance._load_dashboard_section() # Asegurarse de que el dashboard se cargue

            self.page.go("/admin") # Redirige a la ruta de administración
        else:
            logger.warning(f"Login fallido para el usuario: {username}. Credenciales incorrectas.")
            show_snackbar(self.page, "Usuario o contraseña incorrectos.", ft.colors.RED_500)
        self.page.update()

