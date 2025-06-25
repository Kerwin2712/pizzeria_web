# views/main_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_date_picker, create_time_picker, create_message_box

# Aunque los servicios se instanciarán en main.py, los importamos aquí para referencia de tipos
# from services.cliente_service import ClienteService
# from services.menu_service import MenuService
# from services.pedido_service import PedidoService
# from services.financiero_service import FinancieroService
# from services.pizzeria_info_service import PizzeriaInfoService
# from services.administrador_service import AdministradorService

class MainView(ft.View):
    """
    Vista principal de la aplicación de la pizzería.
    Contiene la barra de navegación lateral, la barra superior y el contenido dinámico.
    """
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/" # Ruta por defecto para esta vista

        # Opcional: Instanciar servicios aquí si la vista va a manejar directamente la lógica de DB.
        # Si la lógica de DB se maneja en un controlador o capa superior, estos se pasarán como argumentos.
        # self.cliente_service = ClienteService(page.session_factory) # Suponiendo page.session_factory
        # self.menu_service = MenuService(page.session_factory)

        self.page.title = "La Mejor Pizzería"
        self.page.vertical_alignment = ft.CrossAxisAlignment.START
        self.page.horizontal_alignment = ft.CrossAxisAlignment.START
        self.page.window_height = 800
        self.page.window_width = 1200

        # Contenedor principal para el contenido que cambia dinámicamente
        self.main_content_area = ft.Column(
            expand=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO, # Habilitar scroll si el contenido es grande
            spacing=20,
            controls=[] # Se llenará dinámicamente
        )

        # Barra lateral de navegación
        self.navigation_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True, # Extendida por defecto
            min_width=100,
            min_extended_width=200,
            leading=ft.Container(
                ft.Text("Menú Principal", size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(top=20, bottom=20, left=10)
            ),
            group_alignment=-0.9, # Alinea los ítems en la parte superior
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.HOME_OUTLINED,
                    selected_icon=ft.icons.HOME,
                    label="Inicio",
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.MENU_BOOK_OUTLINED),
                    selected_icon_content=ft.Icon(ft.icons.MENU_BOOK),
                    label="Menú",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SHOPPING_CART_OUTLINED,
                    selected_icon=ft.icons.SHOPPING_CART,
                    label="Hacer Pedido",
                ),
                 ft.NavigationRailDestination(
                    icon=ft.icons.PERSON_ADD_ALT_OUTLINED,
                    selected_icon=ft.icons.PERSON_ADD_ALT,
                    label="Mi Cuenta",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.INFO_OUTLINE,
                    selected_icon=ft.icons.INFO,
                    label="Pizzería Info",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    label="Administrador",
                ),
            ],
            on_change=self._on_navigation_change,
            bgcolor=ft.colors.BLUE_GREY_100, # Color de fondo mejorado
            # border_radius=ft.border_radius.all(10) # Se eliminó esta propiedad, no es soportada directamente por NavigationRail
        )

        # Barra superior (AppBar)
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.LOCAL_PIZZA, size=30),
            leading_width=40,
            title=ft.Text("La Mejor Pizzería", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.BLUE_GREY_900,
            actions=[
                ft.Container(
                    ft.TextField(
                        hint_text="Buscar...",
                        prefix_icon=ft.icons.SEARCH,
                        border_radius=ft.border_radius.all(20),
                        filled=True,
                        fill_color=ft.colors.WHITE,
                        color=ft.colors.BLACK,
                        width=300,
                        on_submit=self._on_search,
                    ),
                    padding=ft.padding.only(right=15)
                ),
                ft.IconButton(ft.icons.HELP_OUTLINE, tooltip="Ayuda"),
                ft.IconButton(ft.icons.MORE_VERT),
            ],
            toolbar_height=70,
            elevation=4
        )

        # Contenido de la vista
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
        
        # Cargar la sección de inicio por defecto
        self._load_home_section()

    def _on_navigation_change(self, e):
        """Maneja el cambio de selección en la barra de navegación lateral."""
        self.navigation_rail.selected_index = e.control.selected_index
        if self.navigation_rail.selected_index == 0:
            self._load_home_section()
        elif self.navigation_rail.selected_index == 1:
            self._load_menu_section()
        elif self.navigation_rail.selected_index == 2:
            self._load_order_section()
        elif self.navigation_rail.selected_index == 3:
            self._load_my_account_section()
        elif self.navigation_rail.selected_index == 4:
            self._load_pizzeria_info_section()
        elif self.navigation_rail.selected_index == 5:
            self._load_admin_section()
        
        self.main_content_area.update()
        self.page.update() # Actualizar la página para reflejar el cambio


    def _on_search(self, e):
        """Maneja la acción de búsqueda."""
        search_query = e.control.value
        show_snackbar(self.page, f"Buscando: {search_query}", ft.colors.BLUE_GREY_700)
        # Aquí iría la lógica para redirigir o filtrar contenido basado en la búsqueda
        # Por ahora, solo muestra un mensaje.

    # --- Secciones de Contenido Dinámico ---

    def _load_home_section(self):
        """Carga la sección de inicio (home)."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="🍕 ¡Bienvenido a La Mejor Pizzería! 🍕",
                content=ft.Column([
                    ft.Text("Las pizzas más deliciosas y el mejor servicio de delivery.", size=18),
                    ft.Text("Explora nuestro menú y haz tu pedido ahora mismo.", size=16),
                    ft.ElevatedButton("Ver Menú", on_click=lambda e: self._on_navigation_change(ft.ControlEvent(control=self.navigation_rail, selected_index=1))),
                    ft.Divider(),
                    ft.Text("Oferta del Día:", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("¡Pizza familiar de Pepperoni con 20% de descuento!", size=16, color=ft.colors.RED_500),
                    ft.Image(
                        src="https://placehold.co/400x200/FF5733/FFFFFF?text=Pizza+Oferta",
                        width=400,
                        height=200,
                        fit=ft.ImageFit.COVER,
                        border_radius=ft.border_radius.all(10)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        )

    def _load_menu_section(self):
        """Carga la sección del menú."""
        self.main_content_area.controls.clear()
        
        # Datos de ejemplo para el menú
        menu_columns = ["Ítem", "Descripción", "Precio"]
        menu_rows = [
            ["Pizza Margarita", "Tomate, mozzarella, albahaca", "$10.50"],
            ["Pizza Pepperoni", "Pepperoni, mozzarella, salsa", "$12.00"],
            ["Pizza Cuatro Quesos", "Mozzarella, provolone, gorgonzola, parmesano", "$13.50"],
            ["Bebida Cola (L)", "Refresco de cola de 1.5L", "$3.00"],
            ["Pan de Ajo", "Pan con ajo y queso fundido", "$4.00"],
            ["Tiramisú", "Postre italiano clásico", "$5.50"],
        ]

        self.main_content_area.controls.append(
            CustomCard(
                title="📜 Nuestro Delicioso Menú 📜",
                content=ft.Column([
                    ft.Text("Aquí puedes encontrar todas nuestras opciones:", size=16),
                    create_data_table(menu_columns, menu_rows),
                    ft.ElevatedButton("Hacer un Pedido", on_click=lambda e: self._on_navigation_change(ft.ControlEvent(control=self.navigation_rail, selected_index=2)))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )

    def _load_order_section(self):
        """Carga la sección para hacer un pedido."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="🛒 Realiza tu Pedido 🛒",
                content=ft.Column([
                    ft.Text("Selecciona tus ítems y completa los datos para el delivery.", size=16),
                    ft.TextField(label="Nombre Completo", hint_text="Juan Pérez"),
                    ft.TextField(label="Dirección de Envío", hint_text="Calle Principal 123, Ciudad"),
                    ft.TextField(label="Teléfono", hint_text="04XX-XXXXXXX"),
                    ft.TextField(label="Email (opcional)", hint_text="correo@example.com"),
                    ft.Divider(),
                    ft.Text("Items del Pedido:", size=18, weight=ft.FontWeight.BOLD),
                    # Aquí iría un ListView o Column de ítems seleccionables del menú
                    ft.ElevatedButton("Añadir Ítem del Menú", on_click=lambda e: show_snackbar(self.page, "Funcionalidad para añadir ítems al carrito.")),
                    ft.Divider(),
                    ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD), # Placeholder para el total
                    ft.ElevatedButton(
                        "Proceder al Pago",
                        icon=ft.icons.PAYMENT,
                        on_click=lambda e: show_alert_dialog(self.page, "Pago", "Funcionalidad de pago no implementada aún.")
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
                width=600
            )
        )

    def _load_my_account_section(self):
        """Carga la sección de Mi Cuenta / Registro de Cliente."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="👤 Mi Cuenta / Regístrate 📝",
                content=ft.Column([
                    ft.Text("¿Ya tienes cuenta? Inicia sesión o regístrate para guardar tus datos y pedidos.", size=16),
                    ft.TextField(label="Email", hint_text="tu_email@example.com"),
                    ft.TextField(label="Contraseña", password=True, can_reveal_password=True),
                    ft.Row([
                        ft.ElevatedButton("Iniciar Sesión", on_click=lambda e: show_snackbar(self.page, "Funcionalidad de inicio de sesión.")),
                        ft.TextButton("Registrarse", on_click=lambda e: show_snackbar(self.page, "Funcionalidad de registro de nuevo cliente."))
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    ft.Text("O regístrate rápidamente:", size=16, weight=ft.FontWeight.BOLD),
                    ft.TextField(label="Nombre Completo"),
                    ft.TextField(label="Cédula"), # Asumiendo que se usa cédula
                    ft.TextField(label="Teléfono"),
                    ft.TextField(label="Dirección"),
                    ft.ElevatedButton("Crear Cuenta", on_click=lambda e: show_snackbar(self.page, "Funcionalidad de creación de cuenta."))
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
                width=600
            )
        )

    def _load_pizzeria_info_section(self):
        """Carga la sección de información de la pizzería."""
        self.main_content_area.controls.clear()
        
        # Datos de ejemplo. Esto se cargaría desde PizzeriaInfoService
        info_nombre = "La Mejor Pizzería C.A."
        info_direccion = "Av. Principal con Calle del Sabor, Centro Comercial Pizza Plaza, Nivel PB, Local #10, Caracas."
        info_telefono = "+58 (212) 123-4567"
        info_email = "contacto@lamejorpizzeria.com"
        info_horario = "Lunes a Domingo: 11:00 AM - 11:00 PM"
        info_facebook = "facebook.com/lamejorpizzeria"
        info_instagram = "instagram.com/lamejorpizzeria"

        self.main_content_area.controls.append(
            CustomCard(
                title="ℹ️ Información de Nuestra Pizzería ℹ️",
                content=ft.Column([
                    ft.Text(f"Nombre: {info_nombre}", size=16),
                    ft.Text(f"Dirección: {info_direccion}", size=16),
                    ft.Text(f"Teléfono: {info_telefono}", size=16),
                    ft.Text(f"Email: {info_email}", size=16),
                    ft.Text(f"Horario: {info_horario}", size=16),
                    ft.Text(f"Síguenos en:"),
                    ft.Row([
                        ft.IconButton(ft.icons.FACEBOOK, url=f"https://{info_facebook}"),
                        ft.GestureDetector( # Nuevo: Para hacer el texto clickeable
                            content=ft.Text(info_facebook, color=ft.colors.BLUE, style=ft.TextThemeStyle.BODY_LARGE),
                            on_tap=lambda e: self.page.launch_url(f"https://{info_facebook}")
                        )
                    ]),
                    ft.Row([
                        ft.IconButton(ft.icons.CAMERA_ALT_ROUNDED, url=f"https://{info_instagram}"),
                        ft.GestureDetector( # Nuevo: Para hacer el texto clickeable
                            content=ft.Text(info_instagram, color=ft.colors.BLUE, style=ft.TextThemeStyle.BODY_LARGE),
                            on_tap=lambda e: self.page.launch_url(f"https://{info_instagram}")
                        )
                    ]),
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=10),
                width=700
            )
        )

    def _load_admin_section(self):
        """Carga la sección de acceso de administrador."""
        self.main_content_area.controls.clear()
        self.main_content_area.controls.append(
            CustomCard(
                title="⚙️ Acceso de Administrador ⚙️",
                content=ft.Column([
                    ft.Text("Por favor, introduce tus credenciales de administrador.", size=16),
                    ft.TextField(label="Usuario", hint_text="admin_user"),
                    ft.TextField(label="Contraseña", password=True, can_reveal_password=True),
                    ft.ElevatedButton(
                        "Iniciar Sesión como Administrador",
                        icon=ft.icons.LOGIN,
                        on_click=lambda e: show_alert_dialog(self.page, "Acceso Admin", "Funcionalidad de inicio de sesión de administrador.")
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=400
            )
        )

# Para probar esta vista, podrías hacer algo como esto en tu main.py:
# import flet as ft
# from views.main_view import MainView

# def main(page: ft.Page):
#     main_view_instance = MainView(page)
#     page.add(main_view_instance)
#     page.go("/") # Asegura que la vista principal sea la que se muestre

# if __name__ == "__main__":
#     ft.app(target=main)
