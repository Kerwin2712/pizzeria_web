# views/main_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_date_picker, create_time_picker, create_message_box, create_simple_bar_chart
import logging # Importa el módulo logging

# Importamos los servicios necesarios
from services.administrador_service import AdministradorService
from services.pizzeria_info_service import PizzeriaInfoService # Importa el nuevo servicio
from services.menu_service import MenuService # Importa MenuService para obtener el menú
from services.cliente_service import ClienteService # Importar ClienteService
from services.pedido_service import PedidoService # Importar PedidoService
from services.financiero_service import FinancieroService # Importar FinancieroService
from views.admin_view import AdminView # Importa AdminView para poder manipular su instancia

logger = logging.getLogger(__name__) # Obtiene una instancia del logger para este módulo

class MainView(ft.View):
    """
    Vista principal de la aplicación de la pizzería.
    Contiene la barra de navegación lateral, la barra superior y el contenido dinámico.
    """
    def __init__(self, page: ft.Page, administrador_service: AdministradorService, admin_view_instance: AdminView, pizzeria_info_service: PizzeriaInfoService, menu_service: MenuService, cliente_service: ClienteService, pedido_service: PedidoService, financiero_service: FinancieroService): # Recibe los nuevos servicios
        super().__init__()
        self.page = page
        self.route = "/" # Ruta por defecto para esta vista

        # Instancia de los servicios
        self.administrador_service = administrador_service
        self.pizzeria_info_service = pizzeria_info_service # Asigna el nuevo servicio
        self.menu_service = menu_service # Asigna el MenuService
        self.cliente_service = cliente_service # Asigna ClienteService
        self.pedido_service = pedido_service # Asigna PedidoService
        self.financiero_service = financiero_service # Asigna FinancieroService
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
        
        # Atributos para la sección de menú que necesitan ser accesibles globalmente en la clase
        self.menu_tabs = None
        self.menu_tab_content_area = None
        self.tab_views_content_list = [] # Lista para almacenar los ft.Column de cada pestaña

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
                    selected_icon_content=ft.Icon(ft.icons.SHOPPING_CART),
                    label="Pedidos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon_content=ft.Icon(ft.icons.ADMIN_PANEL_SETTINGS),
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
        """Carga la sección del menú con pestañas por categoría."""
        logger.info("Cargando sección de menú para el cliente con pestañas.")
        self.main_content_area.controls.clear()

        all_items = self.menu_service.get_all_items_menu()
        all_categories = self.menu_service.get_all_categorias()

        # Agrupar ítems por categoría
        menu_by_category = {}
        # Inicializar menu_by_category con todas las categorías existentes
        for category in all_categories:
            menu_by_category[category.nombre] = []

        if all_items:
            for item in all_items:
                if item.disponible: # Solo mostrar ítems disponibles
                    category_name = item.categoria.nombre if item.categoria else "Sin Categoría"
                    if category_name in menu_by_category:
                        menu_by_category[category_name].append(item)
                    else: # En caso de que un ítem tenga una categoría no registrada previamente
                        menu_by_category[category_name] = [item]
        
        # Crear la lista de pestañas (Tabs) y el contenido de las vistas
        tabs = []
        self.tab_views_content_list = [] # Reiniciar la lista de contenidos de las pestañas
        
        # Pestaña "Todos"
        all_items_content = []
        if all_items:
            for item in all_items:
                if item.disponible:
                    all_items_content.append(self._create_menu_item_card(item))
        else:
            all_items_content.append(ft.Text("¡No hay ítems disponibles en el menú por ahora!", size=16, color=ft.colors.WHITE54))

        tabs.append(ft.Tab(text="Todos"))
        # El scroll se aplica al Column, no al Container que lo envuelve
        self.tab_views_content_list.append(ft.Column(all_items_content, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True))

        # Pestañas por categoría
        for category_name, items in menu_by_category.items():
            tabs.append(ft.Tab(text=category_name))
            category_items_content = []
            if items:
                for item in items:
                    category_items_content.append(self._create_menu_item_card(item))
            else:
                category_items_content.append(ft.Text(f"No hay ítems en la categoría '{category_name}'.", size=14, color=ft.colors.WHITE54))
            
            # El scroll se aplica al Column, no al Container que lo envuelve
            self.tab_views_content_list.append(ft.Column(category_items_content, spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True))

        # El componente Tabs
        self.menu_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=tabs,
            expand=1,
            on_change=self._on_tab_change,
            indicator_color=ft.colors.AMBER_400,
            label_color=ft.colors.WHITE,
            unselected_label_color=ft.colors.WHITE54,
        )

        # El contenedor que mostrará el contenido de la pestaña seleccionada
        # Inicialmente muestra el contenido de la primera pestaña (Todos)
        self.menu_tab_content_area = ft.Container(
            content=self.tab_views_content_list[self.menu_tabs.selected_index],
            expand=True, # Permite que ocupe el espacio disponible
            # Eliminado: scroll=ft.ScrollMode.AUTO de aquí
        )

        self.main_content_area.controls.append(
            CustomCard(
                title="📜 Nuestro Delicioso Menú 📜",
                title_color=self.text_color,
                bgcolor=self.card_bg_color,
                content=ft.Column(
                    [
                        ft.Text("Explora nuestro delicioso menú por categoría. ¡Haz clic para añadir a tu pedido!", size=16, color=self.text_color),
                        self.menu_tabs, # Añadir el componente Tabs
                        self.menu_tab_content_area, # Añadir el área de contenido dinámico
                        ft.Divider(color=ft.colors.BLUE_GREY_700),
                        ft.ElevatedButton(
                            "Ver Pedido / Checkout",
                            icon=ft.icons.SHOPPING_CART_CHECKOUT,
                            on_click=lambda e: self._on_navigation_rail_change(2) # Ir a la sección de pedidos
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                    expand=True # Este expand es para el Column dentro de CustomCard
                ),
                width=800
            )
        )
        self.main_content_area.update()

    def _on_tab_change(self, e):
        """Maneja el cambio de pestaña en la sección del menú."""
        selected_index = e.control.selected_index
        logger.info(f"Pestaña del menú cambiada a índice: {selected_index}")
        # Actualizar el contenido del contenedor principal del menú
        if self.menu_tab_content_area and selected_index < len(self.tab_views_content_list):
            self.menu_tab_content_area.content = self.tab_views_content_list[selected_index]
            self.menu_tab_content_area.update() # Forzar la actualización del contenedor de contenido
        self.page.update()


    def _create_menu_item_card(self, item):
        """Crea una tarjeta (Card) para un ítem del menú."""
        return ft.Card(
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


    def _add_to_order(self, item_id: int, item_name: str, item_price: float):
        """Añade un ítem al pedido del cliente."""
        self.selected_items[item_id] = self.selected_items.get(item_id, 0) + 1
        show_snackbar(self.page, f"'{item_name}' añadido al pedido. Cantidad: {self.selected_items[item_id]}", ft.colors.BLUE_GREY_600)
        logger.info(f"Añadido item {item_name} (ID: {item_id}). Cantidad: {self.selected_items[item_id]}") # Corregido para item_id directamente
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
        self.customer_email_field = ft.TextField(label="Email (opcional)", hint_text="tu@ejemplo.com", filled=True, fill_color=self.textfield_fill_color, color=self.text_color, hint_style=ft.TextStyle(color=ft.colors.WHITE54)) # Nuevo campo para email


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
                    self.customer_phone_field, # Mover teléfono antes del email
                    self.customer_email_field, # Añadir campo de email
                    self.delivery_address_field,
                    ft.ElevatedButton(
                        "Confirmar Pedido",
                        icon=ft.icons.CHECK_CIRCLE,
                        on_click=self._show_payment_options # Llama a la nueva función para mostrar opciones de pago
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

    def _show_payment_options(self, e):
        """Muestra un diálogo para que el cliente elija el método de pago."""
        logger.info("Mostrando opciones de pago.")
        
        self.payment_method = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="Efectivo", label="Efectivo"),
                ft.Radio(value="Pago Móvil", label="Pago Móvil")
            ]),
            value="Efectivo" # Valor por defecto
        )

        def on_payment_selected(e):
            if self.payment_method.value == "Pago Móvil":
                self._display_pago_movil_info()
            else:
                self._hide_pago_movil_info()
            self.page.update()

        self.payment_method.on_change = on_payment_selected

        self.pago_movil_info_display = ft.Column([], visible=False) # Contenedor para la info de Pago Móvil

        # Inicialmente oculta la info de Pago Móvil
        self.pago_movil_info_display.visible = False

        payment_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Selecciona tu Método de Pago", color=self.text_color),
            content=ft.Column([
                self.payment_method,
                self.pago_movil_info_display
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close(payment_dialog)),
                ft.ElevatedButton("Finalizar Pedido", on_click=lambda e: self._confirm_order_with_payment(payment_dialog))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=self.card_bg_color,
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.open(payment_dialog)
        payment_dialog.open = True
        self.page.update()

    def _display_pago_movil_info(self):
        """Muestra la información de Pago Móvil y el botón de WhatsApp."""
        logger.info("Mostrando información de Pago Móvil.")
        info = self.pizzeria_info_service.get_pizzeria_info()
        
        self.pago_movil_info_display.controls.clear()

        if info and info.pago_movil_banco and info.pago_movil_telefono and info.pago_movil_cedula and info.pago_movil_beneficiario:
            self.pago_movil_info_display.controls.extend([
                ft.Divider(),
                ft.Text("Detalles de Pago Móvil:", size=18, weight=ft.FontWeight.BOLD, color=self.text_color),
                ft.Text(f"Banco: {info.pago_movil_banco}", color=self.text_color),
                ft.Text(f"Teléfono: {info.pago_movil_telefono}", color=self.text_color),
                ft.Text(f"Cédula: {info.pago_movil_cedula}", color=self.text_color),
                ft.Text(f"Beneficiario: {info.pago_movil_beneficiario}", color=self.text_color),
            ])
            if info.pago_movil_cuenta:
                 self.pago_movil_info_display.controls.append(ft.Text(f"Cuenta: {info.pago_movil_cuenta}", color=self.text_color))
            
            if info.whatsapp_numero and info.whatsapp_chat_link:
                # Modificación aquí: En lugar de 'url' y 'new_window', usar 'on_click' y 'self.page.launch_url()'
                self.pago_movil_info_display.controls.extend([
                    ft.Divider(),
                    ft.Text("Envía tu comprobante vía WhatsApp:", size=16, color=self.text_color),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon(ft.icons.CHAT),
                            ft.Text(f"Enviar Comprobante al {info.whatsapp_numero}")
                        ]),
                        on_click=lambda e: self.page.launch_url(info.whatsapp_chat_link), # Uso correcto para abrir URL
                        style=ft.ButtonStyle(bgcolor=ft.colors.GREEN_700, color=ft.colors.WHITE)
                    )
                ])
            elif info.whatsapp_numero:
                 self.pago_movil_info_display.controls.extend([
                    ft.Divider(),
                    ft.Text("Envía tu comprobante vía WhatsApp:", size=16, color=self.text_color),
                    ft.Text(f"Número de WhatsApp: {info.whatsapp_numero}", color=self.text_color),
                    ft.Text("El link de chat de WhatsApp no está configurado. Por favor, contacta directamente.", color=ft.colors.YELLOW_500)
                ])
            else:
                self.pago_movil_info_display.controls.append(ft.Text("No hay información de WhatsApp configurada.", color=ft.colors.YELLOW_500))

            self.pago_movil_info_display.visible = True
        else:
            self.pago_movil_info_display.controls.append(ft.Text("Información de Pago Móvil no configurada. Por favor, consulta a la administración.", color=ft.colors.RED_400))
            self.pago_movil_info_display.visible = True # Mostrar el mensaje de error
        
        self.pago_movil_info_display.update() # Asegura que el contenido se actualice

    def _hide_pago_movil_info(self):
        """Oculta la información de Pago Móvil."""
        logger.info("Ocultando información de Pago Móvil.")
        self.pago_movil_info_display.visible = False
        self.pago_movil_info_display.controls.clear()
        self.pago_movil_info_display.update()

    def _confirm_order_with_payment(self, dialog):
        """
        Confirma el pedido con el método de pago seleccionado
        y cierra el diálogo de pago.
        """
        logger.info(f"Confirmando pedido con método de pago: {self.payment_method.value}")
        dialog.open = False # Cerrar el diálogo de selección de pago
        self.page.update()

        customer_name = self.customer_name_field.value
        customer_phone = self.customer_phone_field.value
        customer_email = self.customer_email_field.value
        delivery_address = self.delivery_address_field.value
        metodo_pago = self.payment_method.value # Obtener el método de pago seleccionado

        if not customer_name or not delivery_address or not customer_phone:
            show_snackbar(self.page, "Por favor, completa los campos obligatorios: Nombre, Teléfono y Dirección.", ft.colors.RED_500)
            return
        
        try:
            # 1. Gestionar el cliente: buscar existente o crear nuevo
            cliente = None
            if customer_email:
                cliente = self.cliente_service.get_cliente_by_email(customer_email)
            
            if not cliente:
                clientes_por_telefono = self.cliente_service.search_clientes(query=customer_phone)
                if clientes_por_telefono:
                    cliente_match = next((c for c in clientes_por_telefono if c.nombre.lower() == customer_name.lower()), None)
                    if cliente_match:
                        cliente = cliente_match
                        logger.info(f"Cliente existente encontrado por nombre y teléfono con ID: {cliente.id}")
                
                if not cliente: # Si aún no se encontró, crear un nuevo cliente
                    logger.info(f"Cliente no encontrado. Creando nuevo cliente: {customer_name}")
                    cliente_data = {
                        'nombre': customer_name,
                        'telefono': customer_phone,
                        'direccion': delivery_address
                    }
                    if customer_email:
                        cliente_data['email'] = customer_email
                    
                    cliente = self.cliente_service.add_cliente(cliente_data)
                    if not cliente:
                        show_snackbar(self.page, "Error al registrar un nuevo cliente.", ft.colors.RED_500)
                        logger.error("Fallo al añadir nuevo cliente.")
                        return

            logger.info(f"Cliente final para el pedido con ID: {cliente.id}")

            # 2. Preparar ítems para el pedido
            items_para_pedido = []
            for item_id, quantity in self.selected_items.items():
                items_para_pedido.append({'item_id': item_id, 'cantidad': quantity})

            # Calcular el total del pedido antes de añadirlo (podría ser redundante si el servicio ya lo hace, pero es buena práctica)
            total_pedido_calculated = sum(self.menu_service.get_item_menu_by_id(item_id).precio * quantity for item_id, quantity in self.selected_items.items() if self.menu_service.get_item_menu_by_id(item_id))


            # 3. Añadir el pedido a la base de datos, incluyendo el método de pago
            nuevo_pedido = self.pedido_service.add_pedido(
                cliente_id=cliente.id,
                direccion_delivery=delivery_address,
                items_con_cantidad=items_para_pedido,
                total=total_pedido_calculated, # Asegúrate que el servicio acepte 'total' como argumento
                metodo_pago=metodo_pago # Pasa el método de pago
            )

            if nuevo_pedido:
                # 4. Registrar la transacción financiera (ingreso)
                self.financiero_service.add_registro(
                    tipo='Ingreso',
                    monto=nuevo_pedido.total,
                    descripcion=f"Venta de pedido #{nuevo_pedido.id} ({metodo_pago}) a {cliente.nombre}",
                    pedido_id=nuevo_pedido.id
                )
                show_snackbar(self.page, f"¡Pedido #{nuevo_pedido.id} realizado con éxito para {cliente.nombre}! Total: ${nuevo_pedido.total:,.2f} ({metodo_pago})", ft.colors.GREEN_700)
                logger.info(f"Pedido #{nuevo_pedido.id} completado y registrado. Cliente: {cliente.nombre}, Total: {nuevo_pedido.total}, Método: {metodo_pago}")

                # Limpiar el carrito y campos de formulario después del pedido exitoso
                self.selected_items.clear()
                self.customer_name_field.value = ""
                self.customer_phone_field.value = ""
                self.customer_email_field.value = ""
                self.delivery_address_field.value = ""

                self._load_home_section() # Redirigir al inicio
            else:
                show_snackbar(self.page, "Error al crear el pedido. Por favor, inténtalo de nuevo.", ft.colors.RED_500)
                logger.error("Fallo al añadir el pedido a la base de datos.")

        except Exception as ex:
            show_snackbar(self.page, f"Ocurrió un error inesperado al procesar el pedido: {ex}", ft.colors.RED_700)
            logger.exception("Error inesperado en _confirm_order_with_payment:")
        
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

