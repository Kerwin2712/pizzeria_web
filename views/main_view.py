# views/main_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_date_picker, create_time_picker, create_message_box, create_simple_bar_chart
import logging # Importa el módulo logging

# Importamos los servicios necesarios
from services.administrador_service import AdministradorService
from services.pizzeria_info_service import PizzeriaInfoService # Importa el nuevo servicio
from services.menu_service import MenuService # Importa MenuService para obtener el menú
from views.admin_view import AdminView # Importa AdminView para poder manipular su instancia

logger = logging.getLogger(__name__) # Obtiene una instancia del logger para este módulo

class MainView(ft.View):
    """
    Vista principal de la aplicación de la pizzería.
    Contiene la barra de navegación lateral, la barra superior y el contenido dinámico.
    """
    def __init__(self, page: ft.Page, administrador_service: AdministradorService, admin_view_instance: AdminView, pizzeria_info_service: PizzeriaInfoService, menu_service: MenuService): # Recibe el nuevo servicio
        super().__init__()
        self.page = page
        self.route = "/" # Ruta por defecto para esta vista

        # Instancia de los servicios
        self.administrador_service = administrador_service
        self.pizzeria_info_service = pizzeria_info_service # Asigna el nuevo servicio
        self.menu_service = menu_service # Asigna el MenuService
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
        self.selected_items = {} # Diccionario para almacenar ítems seleccionados para el pedido: {item_id: cantidad}

        # Define el NavRail y su contenido
        self.navigation_rail = self._create_navigation_rail()

        # Define el AppBar
        self.appbar = ft.AppBar(
            title=ft.Text("Pizzería Acme", color=ft.colors.WHITE),
            center_title=True,
            bgcolor=ft.colors.BLUE_GREY_900,
            actions=[
                ft.IconButton(
                    icon=ft.icons.INFO_OUTLINE,
                    tooltip="Acerca de",
                    on_click=lambda e: show_snackbar(self.page, "Aplicación de Pizzería Flet v1.0", ft.colors.BLUE_GREY_500)
                ),
            ]
        )

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
            self.appbar, # Agregamos el AppBar aquí
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
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    label="Administrador",
                ),
            ],
            on_change=self._on_navigation_rail_change,
        )

    def _on_navigation_rail_change(self, e):
        """Maneja el cambio de selección en el NavRail.
        
        Modificado para aceptar directamente el índice o un objeto de evento.
        """
        # Verifica si e es un entero (directamente el índice) o un objeto ControlEvent
        if isinstance(e, int):
            selected_index = e
        else: # Asume que es un ControlEvent
            selected_index = e.control.selected_index
        
        logger.info(f"Navegación seleccionada: {selected_index}")
        self.navigation_rail.selected_index = selected_index # Actualiza el índice seleccionado
        if selected_index == 0:
            self._load_home_section()
        elif selected_index == 1:
            self._load_menu_section() # Puedes definir esta función
        elif selected_index == 2:
            self._load_orders_section() # Puedes definir esta función
        elif selected_index == 3: # Índice para administrador
            self._load_admin_section()
        self.page.update()

    def _load_home_section(self):
        """Carga la sección de inicio."""
        self.main_content_area.controls.clear()

        pizzeria_info = self.pizzeria_info_service.get_pizzeria_info()
        
        # Contenido dinámico basado en la información de la pizzería
        pizzeria_details = []
        if pizzeria_info:
            pizzeria_details.extend([
                ft.Text(f"Nombre: {pizzeria_info.nombre_pizzeria}", size=16, color=self.text_color),
                ft.Text(f"Dirección: {pizzeria_info.direccion}", size=16, color=self.text_color),
                ft.Text(f"Teléfono: {pizzeria_info.telefono}", size=16, color=self.text_color),
            ])
            if pizzeria_info.email_contacto:
                pizzeria_details.append(ft.Text(f"Email: {pizzeria_info.email_contacto}", size=16, color=self.text_color))
            if pizzeria_info.horario_atencion:
                pizzeria_details.append(ft.Text(f"Horario: {pizzeria_info.horario_atencion}", size=16, color=self.text_color))
            if pizzeria_info.red_social_facebook or pizzeria_info.red_social_instagram:
                social_links = []
                if pizzeria_info.red_social_facebook:
                    social_links.append(ft.IconButton(
                        icon=ft.icons.FACEBOOK,
                        url=pizzeria_info.red_social_facebook,
                        tooltip="Facebook",
                        icon_color=ft.colors.BLUE_600
                    ))
                if pizzeria_info.red_social_instagram:
                    social_links.append(ft.IconButton(
                        icon=ft.icons.CAMERA_ALT_ROUNDED,
                        url=pizzeria_info.red_social_instagram,
                        tooltip="Instagram",
                        icon_color=ft.colors.PINK_400
                    ))
                pizzeria_details.append(ft.Row(social_links, alignment=ft.MainAxisAlignment.CENTER))
        else:
            pizzeria_details.append(ft.Text("Información de la pizzería no disponible. Por favor, configúrala en el panel de administración.", size=16, color=ft.colors.RED_400))


        self.main_content_area.controls.append(
            CustomCard(
                title="🍕 ¡Bienvenido a la Pizzería Acme! 🍕",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column(
                    [
                        ft.Text("Explora nuestro delicioso menú o gestiona tu pedido.", size=16, color=self.text_color),
                        ft.Text("¡Tu destino favorito para las mejores pizzas!", size=16, color=self.text_color),
                        ft.Divider(color=ft.colors.BLUE_GREY_700),
                        ft.Text("Nuestra Pizzería:", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
                        *pizzeria_details, # Desempaqueta la lista de detalles de la pizzería aquí
                        ft.Divider(color=ft.colors.BLUE_GREY_700),
                        ft.Text("Oferta del Día:", size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
                        ft.Text("¡Pizza Grande de Pepperoni con un 20% de descuento!", size=16, color=ft.colors.RED_500),
                        ft.Image(
                            src="https://placehold.co/400x200/FF5733/FFFFFF?text=Pizza+Oferta",
                            width=400,
                            height=200,
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(10)
                        ),
                        # Botón para ver el menú
                        ft.ElevatedButton("Ver Menú", on_click=lambda e: self._on_navigation_rail_change(1)),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        )
        self.main_content_area.update() # Asegura que la UI se actualice

    def _load_menu_section(self):
        """Carga la sección del menú."""
        logger.info("Cargando sección de menú para el cliente.")
        self.main_content_area.controls.clear()

        all_items = self.menu_service.get_all_items_menu()
        
        # Agrupar ítems por categoría
        menu_by_category = {}
        if all_items:
            for item in all_items:
                if item.disponible: # Solo mostrar ítems disponibles
                    category_name = item.categoria.nombre if item.categoria else "Sin Categoría"
                    if category_name not in menu_by_category:
                        menu_by_category[category_name] = []
                    menu_by_category[category_name].append(item)
        
        menu_content = []
        menu_content.append(ft.Text("Explora nuestro delicioso menú. ¡Haz clic para añadir a tu pedido!", size=16, color=self.text_color))

        # Iterar sobre categorías y sus ítems
        for category, items in menu_by_category.items():
            menu_content.append(ft.Divider(color=ft.colors.BLUE_GREY_700))
            menu_content.append(ft.Text(category, size=24, weight=ft.FontWeight.BOLD, color=self.text_color))
            menu_content.append(ft.Divider(color=ft.colors.BLUE_GREY_700))

            for item in items:
                # Usar un Card para cada ítem del menú
                menu_content.append(
                    ft.Card(
                        elevation=3,
                        content=ft.Container(
                            padding=15,
                            content=ft.Row([
                                ft.Image(
                                    src=item.imagen_url if item.imagen_url else "https://placehold.co/100x100/343a40/FFFFFF?text=No+Img",
                                    width=100,
                                    height=100,
                                    fit=ft.ImageFit.COVER,
                                    border_radius=ft.border_radius.all(10),
                                    error_content=ft.Icon(ft.icons.BROKEN_IMAGE, color=ft.colors.RED_400, size=50) # Icono si la imagen no carga
                                ),
                                ft.Column([
                                    ft.Text(item.nombre, size=20, weight=ft.FontWeight.BOLD, color=self.text_color),
                                    ft.Text(item.descripcion if item.descripcion else "Sin descripción.", size=14, color=ft.colors.WHITE70),
                                    ft.Text(f"${item.precio:,.2f}", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_400),
                                ],
                                expand=True,
                                spacing=5),
                                ft.Column([
                                    ft.IconButton(
                                        icon=ft.icons.ADD_SHOPPING_CART,
                                        tooltip="Añadir al Pedido",
                                        icon_color=ft.colors.BLUE_400,
                                        on_click=lambda e, item_id=item.id, item_name=item.nombre, item_price=item.precio: self._add_to_order(item_id, item_name, item_price)
                                    ),
                                    ft.Text(str(self.selected_items.get(item.id, 0)), size=16, color=self.text_color, text_align=ft.TextAlign.CENTER),
                                    ft.IconButton(
                                        icon=ft.icons.REMOVE_SHOPPING_CART,
                                        tooltip="Quitar del Pedido",
                                        icon_color=ft.colors.RED_400,
                                        on_click=lambda e, item_id=item.id: self._remove_from_order(item_id)
                                    ),
                                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.CENTER)
                        ),
                        color=self.card_bg_color # Color de fondo de la tarjeta
                    )
                )
        
        if not menu_by_category:
            menu_content.append(ft.Text("¡No hay ítems disponibles en el menú por ahora!", size=16, color=ft.colors.WHITE54))

        menu_content.append(ft.Divider(color=ft.colors.BLUE_GREY_700))
        menu_content.append(ft.ElevatedButton(
            "Ver Pedido / Checkout",
            icon=ft.icons.SHOPPING_CART_CHECKOUT,
            on_click=lambda e: self._on_navigation_rail_change(2) # Ir a la sección de pedidos
        ))

        self.main_content_area.controls.append(
            CustomCard(
                title="📜 Nuestro Delicioso Menú 📜",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column(
                    menu_content,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15
                ),
                width=800
            )
        )
        self.main_content_area.update()

    def _add_to_order(self, item_id: int, item_name: str, item_price: float):
        """Añade un ítem al pedido del cliente."""
        self.selected_items[item_id] = self.selected_items.get(item_id, 0) + 1
        show_snackbar(self.page, f"'{item_name}' añadido al pedido. Cantidad: {self.selected_items[item_id]}", ft.colors.BLUE_GREY_600)
        logger.info(f"Añadido item {item_name} (ID: {item_id}). Cantidad: {self.selected_items[item_id]}")
        self._load_menu_section() # Recargar la sección del menú para actualizar las cantidades
        # No llamar a page.update() aquí, lo hará _load_menu_section()

    def _remove_from_order(self, item_id: int):
        """Remueve un ítem del pedido del cliente."""
        if item_id in self.selected_items:
            self.selected_items[item_id] -= 1
            if self.selected_items[item_id] <= 0:
                del self.selected_items[item_id]
                show_snackbar(self.page, "Ítem removido del pedido.", ft.colors.AMBER_600)
                logger.info(f"Removido item ID: {item_id}. Cantidad: 0.")
            else:
                item_name = self.menu_service.get_item_menu_by_id(item_id).nombre # Obtener nombre para snackbar
                show_snackbar(self.page, f"Cantidad de '{item_name}' reducida. Cantidad: {self.selected_items[item_id]}", ft.colors.AMBER_600)
                logger.info(f"Cantidad de item ID: {item_id} reducida. Cantidad: {self.selected_items[item_id]}.")
        else:
            show_snackbar(self.page, "El ítem no está en tu pedido.", ft.colors.RED_500)
            logger.warning(f"Intento de remover ítem ID: {item_id} que no está en el pedido.")
        self._load_menu_section() # Recargar la sección del menú para actualizar las cantidades

    def _load_orders_section(self):
        """Carga la sección de pedidos."""
        logger.info("Cargando sección de pedidos para el cliente.")
        self.main_content_area.controls.clear()

        # Mostrar ítems seleccionados
        order_items_display = []
        total_order_price = 0.0

        if not self.selected_items:
            order_items_display.append(ft.Text("Tu carrito está vacío. ¡Explora nuestro menú!", size=16, color=self.text_color))
        else:
            order_items_display.append(ft.Text("Detalles de tu Pedido:", size=20, weight=ft.FontWeight.BOLD, color=self.text_color))
            for item_id, quantity in self.selected_items.items():
                item = self.menu_service.get_item_menu_by_id(item_id)
                if item:
                    item_total = item.precio * quantity
                    total_order_price += item_total
                    order_items_display.append(
                        ft.Row([
                            ft.Text(f"{quantity} x {item.nombre}", expand=True, color=self.text_color),
                            ft.Text(f"${item_total:,.2f}", color=self.text_color),
                            ft.IconButton(
                                icon=ft.icons.DELETE_FOREVER,
                                tooltip="Quitar todo el ítem",
                                icon_color=ft.colors.RED_700,
                                on_click=lambda e, item_id=item.id: self._remove_all_of_item(item_id)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                    )
            
            order_items_display.append(ft.Divider(color=ft.colors.BLUE_GREY_700))
            order_items_display.append(
                ft.Row([
                    ft.Text("Total del Pedido:", size=22, weight=ft.FontWeight.BOLD, color=self.text_color),
                    ft.Text(f"${total_order_price:,.2f}", size=22, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_500)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )

        # Campos para información del cliente y dirección
        self.customer_name_field = ft.TextField(label="Nombre Completo", hint_text="Juan Pérez", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.delivery_address_field = ft.TextField(label="Dirección de Envío", hint_text="Calle Falsa 123, Springfield", multiline=True, filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))
        self.customer_phone_field = ft.TextField(label="Teléfono", hint_text="04XX-XXXXXXX", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54))


        self.main_content_area.controls.append(
            CustomCard(
                title="🛒 Realiza tu Pedido 🛒",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column([
                    ft.Text("Completa los detalles para tu pedido y dirección de envío.", size=16, color=self.text_color),
                    *order_items_display, # Muestra los ítems del carrito
                    ft.Divider(color=ft.colors.BLUE_GREY_700),
                    self.customer_name_field,
                    self.delivery_address_field,
                    self.customer_phone_field,
                    ft.ElevatedButton(
                        "Confirmar Pedido",
                        icon=ft.icons.CHECK_CIRCLE,
                        on_click=self._confirm_order # Llama a la nueva función para confirmar el pedido
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15),
                width=600
            )
        )
        self.main_content_area.update()

    def _remove_all_of_item(self, item_id: int):
        """Elimina todas las unidades de un ítem del pedido."""
        if item_id in self.selected_items:
            item_name = self.menu_service.get_item_menu_by_id(item_id).nombre # Obtener nombre para snackbar
            del self.selected_items[item_id]
            show_snackbar(self.page, f"Todas las unidades de '{item_name}' removidas del pedido.", ft.colors.AMBER_700)
            logger.info(f"Todas las unidades de item ID: {item_id} removidas.")
        self._load_orders_section() # Recargar la sección de pedidos para actualizar la vista

    def _confirm_order(self, e):
        """Maneja la confirmación de un pedido por parte del cliente."""
        logger.info("Intentando confirmar pedido.")
        if not self.selected_items:
            show_snackbar(self.page, "Tu carrito está vacío. Añade ítems al menú antes de confirmar.", ft.colors.RED_500)
            return

        customer_name = self.customer_name_field.value
        delivery_address = self.delivery_address_field.value
        customer_phone = self.customer_phone_field.value

        if not customer_name or not delivery_address or not customer_phone:
            show_snackbar(self.page, "Por favor, completa todos los campos de contacto y dirección.", ft.colors.RED_500)
            return
        
        # Calcular el total del pedido
        total_order_price = 0.0
        for item_id, quantity in self.selected_items.items():
            item = self.menu_service.get_item_menu_by_id(item_id)
            if item:
                total_order_price += item.precio * quantity

        # Aquí integrarías la lógica real para guardar el pedido en la base de datos.
        # Por ahora, es un mensaje simulado.
        show_snackbar(self.page, f"¡Pedido de ${total_order_price:,.2f} realizado con éxito a {delivery_address} para {customer_name}!", ft.colors.GREEN_700)
        logger.info(f"Pedido simulado realizado. Cliente: {customer_name}, Total: {total_order_price}")

        # Limpiar el carrito después del pedido
        self.selected_items.clear()
        self._load_home_section() # Redirigir al inicio o a una página de confirmación
        self.page.update()


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

