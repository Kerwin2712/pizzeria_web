# views/admin_view.py
import flet as ft
from utils.widgets import CustomCard, create_data_table, show_snackbar, show_alert_dialog, create_message_box, create_simple_bar_chart
from datetime import datetime, date

# Importaciones de servicios (estos se pasarán al constructor)
from services.cliente_service import ClienteService
from services.menu_service import MenuService
from services.pedido_service import PedidoService
from services.financiero_service import FinancieroService
from services.pizzeria_info_service import PizzeriaInfoService
from services.administrador_service import AdministradorService

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

        # Servicios de base de datos
        self.cliente_service = cliente_service
        self.menu_service = menu_service
        self.pedido_service = pedido_service
        self.financiero_service = financiero_service
        self.pizzeria_info_service = pizzeria_info_service
        self.administrador_service = administrador_service

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
                ft.Text("Gestión", size=18, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(top=20, bottom=20, left=10)
            ),
            group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD_OUTLINED,
                    selected_icon=ft.icons.DASHBOARD,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MENU_BOOK_OUTLINED,
                    selected_icon=ft.icons.MENU_BOOK,
                    label="Menú",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE_OUTLINED,
                    selected_icon=ft.icons.PEOPLE,
                    label="Clientes",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.RECEIPT_OUTLINED,
                    selected_icon=ft.icons.RECEIPT,
                    label="Pedidos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.MONEY_OUTLINED,
                    selected_icon=ft.icons.MONEY,
                    label="Finanzas",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.BUSINESS_OUTLINED,
                    selected_icon=ft.icons.BUSINESS,
                    label="Info Pizzería",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.ADMIN_PANEL_SETTINGS_OUTLINED,
                    selected_icon=ft.icons.ADMIN_PANEL_SETTINGS,
                    label="Administradores",
                ),
            ],
            on_change=self._on_navigation_change,
            bgcolor=ft.colors.GREY_100,
        )

        # Barra superior para la vista de administrador
        self.page.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.SETTINGS, size=30),
            leading_width=40,
            title=ft.Text("Panel de Administración", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.BLUE_GREY_900,
            actions=[
                ft.IconButton(ft.icons.LOGOUT, tooltip="Cerrar Sesión", on_click=self._logout),
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
                    self.admin_content_area,
                ],
                expand=True,
            )
        ]
        
        # Cargar la sección de dashboard por defecto
        self._load_dashboard_section()

    def _logout(self, e):
        """Cierra la sesión del administrador y regresa a la vista principal."""
        show_snackbar(self.page, "Sesión de administrador cerrada.", ft.colors.AMBER_700)
        # Aquí se debería redirigir a la vista principal o a la pantalla de login del cliente
        self.page.go("/") # Redirige a la ruta principal de la aplicación
        self.page.update()

    def _on_navigation_change(self, e):
        """Maneja el cambio de selección en la barra de navegación lateral del administrador."""
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
        
        self.admin_content_area.update()
        self.page.update()

    # --- Secciones de Gestión ---

    def _load_dashboard_section(self):
        """
        Carga la sección del Dashboard con un resumen rápido.
        """
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
                ft.Text("Dashboard de Administración", size=28, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Row([
                    CustomCard(
                        title="Clientes Registrados",
                        content=ft.Text(str(num_clientes), size=40, weight=ft.FontWeight.BOLD),
                        width=250, height=150
                    ),
                    CustomCard(
                        title="Pedidos Pendientes",
                        content=ft.Text(str(num_pedidos_pendientes), size=40, weight=ft.FontWeight.BOLD),
                        width=250, height=150
                    ),
                    CustomCard(
                        title="Ingresos Hoy",
                        content=ft.Text(f"${ingresos_hoy:,.2f}", size=40, weight=ft.FontWeight.BOLD),
                        width=250, height=150
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    CustomCard(
                        title="Gastos Hoy",
                        content=ft.Text(f"${gastos_hoy:,.2f}", size=40, weight=ft.FontWeight.BOLD),
                        width=250, height=150
                    ),
                    CustomCard(
                        title="Balance Hoy",
                        content=ft.Text(f"${balance_hoy:,.2f}", size=40, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700 if balance_hoy >= 0 else ft.colors.RED_700),
                        width=250, height=150
                    ),
                    CustomCard(
                        title="Pedidos Completados",
                        content=ft.Text(str(num_pedidos_completados), size=40, weight=ft.FontWeight.BOLD),
                        width=250, height=150
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                create_simple_bar_chart(sales_data, "Ventas de la Semana (Ejemplo)")
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True)
        )

    def _load_menu_management(self):
        """Carga la sección para gestionar el menú (categorías e ítems)."""
        self.admin_content_area.controls.clear()
        
        # --- Gestión de Categorías ---
        categories = self.menu_service.get_all_categorias()
        cat_columns = ["ID", "Nombre", "Descripción"]
        cat_rows = []
        if categories:
            for cat in categories:
                cat_rows.append([str(cat.id), cat.nombre, cat.descripcion if cat.descripcion else ""])

        self.admin_content_area.controls.append(
            CustomCard(
                title="🍕 Gestión de Categorías del Menú 🍕",
                content=ft.Column([
                    ft.Text("Aquí puedes añadir, editar o eliminar categorías del menú.", size=16),
                    create_data_table(cat_columns, cat_rows),
                    ft.Row([
                        ft.ElevatedButton("Añadir Categoría", on_click=self._open_add_edit_categoria_dialog),
                        # ft.ElevatedButton("Editar Categoría", on_click=self._open_add_edit_categoria_dialog), # Implementar edición
                        # ft.ElevatedButton("Eliminar Categoría", on_click=self._confirm_delete_categoria), # Implementar eliminación
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )

        # --- Gestión de Ítems del Menú ---
        items = self.menu_service.get_all_items_menu()
        item_columns = ["ID", "Nombre", "Precio", "Categoría", "Disponible"]
        item_rows = []
        if items:
            for item in items:
                # Obtener el nombre de la categoría
                cat_name = ""
                if item.categoria:
                    cat_name = item.categoria.nombre
                
                item_rows.append([str(item.id), item.nombre, f"${item.precio:,.2f}", cat_name, "Sí" if item.disponible else "No"])

        self.admin_content_area.controls.append(
            CustomCard(
                title="🍔 Gestión de Ítems del Menú 🍟",
                content=ft.Column([
                    ft.Text("Aquí puedes gestionar los ítems específicos de tu menú.", size=16),
                    create_data_table(item_columns, item_rows),
                    ft.Row([
                        ft.ElevatedButton("Añadir Ítem", on_click=self._open_add_edit_item_dialog),
                        # ft.ElevatedButton("Editar Ítem", on_click=self._open_add_edit_item_dialog), # Implementar edición
                        # ft.ElevatedButton("Eliminar Ítem", on_click=self._confirm_delete_item), # Implementar eliminación
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )
    
    def _open_add_edit_categoria_dialog(self, e):
        """Abre un diálogo para añadir o editar una categoría."""
        nombre_field = ft.TextField(label="Nombre de la Categoría", required=True)
        descripcion_field = ft.TextField(label="Descripción (opcional)", multiline=True)

        def save_categoria(e):
            if not nombre_field.value:
                show_snackbar(self.page, "El nombre de la categoría es requerido.", ft.colors.RED_500)
                return

            new_cat = self.menu_service.add_categoria(nombre_field.value, descripcion_field.value)
            if new_cat:
                show_snackbar(self.page, f"Categoría '{new_cat.nombre}' añadida con éxito.", ft.colors.GREEN_500)
                self.page.close_dialog(dialog) # Cierra el diálogo
                self._load_menu_management() # Recarga la sección para mostrar los cambios
            else:
                show_snackbar(self.page, "Error al añadir la categoría.", ft.colors.RED_500)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Añadir Nueva Categoría"),
            content=ft.Column([
                nombre_field,
                descripcion_field
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog(dialog)),
                ft.ElevatedButton("Guardar", on_click=save_categoria)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _open_add_edit_item_dialog(self, e):
        """Abre un diálogo para añadir o editar un ítem del menú."""
        nombre_field = ft.TextField(label="Nombre del Ítem", required=True)
        descripcion_field = ft.TextField(label="Descripción (opcional)", multiline=True)
        precio_field = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER, required=True)
        imagen_url_field = ft.TextField(label="URL de Imagen (opcional)")
        disponible_checkbox = ft.Checkbox(label="Disponible", value=True)

        categorias = self.menu_service.get_all_categorias()
        categoria_dropdown_options = [ft.dropdown.Option(str(c.id), c.nombre) for c in categorias]
        categoria_dropdown = ft.Dropdown(
            label="Categoría",
            options=categoria_dropdown_options,
            required=True
        )

        def save_item(e):
            try:
                precio = float(precio_field.value)
            except ValueError:
                show_snackbar(self.page, "El precio debe ser un número válido.", ft.colors.RED_500)
                return

            if not nombre_field.value or not categoria_dropdown.value:
                show_snackbar(self.page, "Nombre y Categoría son requeridos.", ft.colors.RED_500)
                return

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
                self.page.close_dialog(dialog)
                self._load_menu_management()
            else:
                show_snackbar(self.page, "Error al añadir el ítem.", ft.colors.RED_500)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Añadir Nuevo Ítem al Menú"),
            content=ft.Column([
                nombre_field,
                descripcion_field,
                precio_field,
                imagen_url_field,
                disponible_checkbox,
                categoria_dropdown
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.page.close_dialog(dialog)),
                ft.ElevatedButton("Guardar", on_click=save_item)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15))
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def _load_client_management(self):
        """Carga la sección para gestionar clientes."""
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
                content=ft.Column([
                    ft.Text("Gestiona los clientes registrados en tu pizzería.", size=16),
                    create_data_table(client_columns, client_rows),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Cliente", on_click=lambda e: show_snackbar(self.page, "Añadir cliente - implementar.")),
                        # ft.ElevatedButton("Editar Cliente", on_click=lambda e: show_snackbar(self.page, "Editar cliente - implementar.")),
                        # ft.ElevatedButton("Eliminar Cliente", on_click=lambda e: show_snackbar(self.page, "Eliminar cliente - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )

    def _load_order_management(self):
        """Carga la sección para gestionar pedidos."""
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
                content=ft.Column([
                    ft.Text("Monitorea y gestiona el estado de todos los pedidos.", size=16),
                    create_data_table(order_columns, order_rows),
                    ft.Row([
                        # ft.ElevatedButton("Ver Detalles", on_click=lambda e: show_snackbar(self.page, "Ver detalles de pedido - implementar.")),
                        # ft.ElevatedButton("Actualizar Estado", on_click=lambda e: show_snackbar(self.page, "Actualizar estado de pedido - implementar.")),
                        # ft.ElevatedButton("Eliminar Pedido", on_click=lambda e: show_snackbar(self.page, "Eliminar pedido - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )

    def _load_finance_management(self):
        """Carga la sección para gestionar las finanzas (ingresos/gastos)."""
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
        last_day_of_month = date(today.year, today.month, 28) # Simplificado, mejor usar calendar.monthrange
        
        total_ingresos_mes = self.financiero_service.get_total_ingresos(first_day_of_month, last_day_of_month)
        total_gastos_mes = self.financiero_service.get_total_gastos(first_day_of_month, last_day_of_month)
        balance_mes = total_ingresos_mes - total_gastos_mes


        self.admin_content_area.controls.append(
            CustomCard(
                title="💰 Gestión de Finanzas 📊",
                content=ft.Column([
                    ft.Text("Registros de ingresos y gastos de la pizzería.", size=16),
                    ft.Row([
                        CustomCard(
                            title=f"Ingresos {today.strftime('%B')}",
                            content=ft.Text(f"${total_ingresos_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD),
                            width=200, height=120
                        ),
                        CustomCard(
                            title=f"Gastos {today.strftime('%B')}",
                            content=ft.Text(f"${total_gastos_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD),
                            width=200, height=120
                        ),
                        CustomCard(
                            title=f"Balance {today.strftime('%B')}",
                            content=ft.Text(f"${balance_mes:,.2f}", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN_700 if balance_mes >= 0 else ft.colors.RED_700),
                            width=200, height=120
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Divider(),
                    create_data_table(finance_columns, finance_rows),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Registro", on_click=lambda e: show_snackbar(self.page, "Añadir registro financiero - implementar.")),
                        # ft.ElevatedButton("Editar Registro", on_click=lambda e: show_snackbar(self.page, "Editar registro financiero - implementar.")),
                        # ft.ElevatedButton("Eliminar Registro", on_click=lambda e: show_snackbar(self.page, "Eliminar registro financiero - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=1000
            )
        )

    def _load_pizzeria_info_management(self):
        """Carga la sección para gestionar la información de la pizzería."""
        self.admin_content_area.controls.clear()
        
        info = self.pizzeria_info_service.get_pizzeria_info()
        
        nombre_field = ft.TextField(label="Nombre de la Pizzería", value=info.nombre_pizzeria if info else "", required=True)
        direccion_field = ft.TextField(label="Dirección", value=info.direccion if info else "", multiline=True, required=True)
        telefono_field = ft.TextField(label="Teléfono", value=info.telefono if info else "", required=True)
        email_field = ft.TextField(label="Email de Contacto", value=info.email_contacto if info else "")
        horario_field = ft.TextField(label="Horario de Atención", value=info.horario_atencion if info else "", multiline=True)
        facebook_field = ft.TextField(label="URL Facebook", value=info.red_social_facebook if info else "")
        instagram_field = ft.TextField(label="URL Instagram", value=info.red_social_instagram if info else "")

        def save_pizzeria_info(e):
            if not nombre_field.value or not direccion_field.value or not telefono_field.value:
                show_snackbar(self.page, "Nombre, Dirección y Teléfono son requeridos.", ft.colors.RED_500)
                return

            if info: # Si ya existe, actualiza
                info.nombre_pizzeria = nombre_field.value
                info.direccion = direccion_field.value
                info.telefono = telefono_field.value
                info.email_contacto = email_field.value
                info.horario_atencion = horario_field.value
                info.red_social_facebook = facebook_field.value
                info.red_social_instagram = instagram_field.value
                updated_info = self.pizzeria_info_service.update_pizzeria_info(info)
                if updated_info:
                    show_snackbar(self.page, "Información de la pizzería actualizada con éxito.", ft.colors.GREEN_500)
                else:
                    show_snackbar(self.page, "Error al actualizar la información.", ft.colors.RED_500)
            else: # Si no existe, añade una nueva
                new_info = self.pizzeria_info_service.add_pizzeria_info(
                    nombre_pizzeria=nombre_field.value,
                    direccion=direccion_field.value,
                    telefono=telefono_field.value,
                    email_contacto=email_field.value,
                    horario_atencion=horario_field.value,
                    red_social_facebook=facebook_field.value,
                    red_social_instagram=instagram_field.value
                )
                if new_info:
                    show_snackbar(self.page, "Información de la pizzería añadida con éxito.", ft.colors.GREEN_500)
                    # Recargar la sección para que los campos se muestren con los nuevos valores
                    self._load_pizzeria_info_management()
                else:
                    show_snackbar(self.page, "Error al añadir la información inicial.", ft.colors.RED_500)
            self.page.update()

        self.admin_content_area.controls.append(
            CustomCard(
                title="🏢 Gestión de Información de la Pizzería 📋",
                content=ft.Column([
                    ft.Text("Actualiza la información visible al público de tu pizzería.", size=16),
                    nombre_field,
                    direccion_field,
                    telefono_field,
                    email_field,
                    horario_field,
                    facebook_field,
                    instagram_field,
                    ft.ElevatedButton("Guardar Cambios", on_click=save_pizzeria_info)
                ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=15),
                width=600
            )
        )

    def _load_admin_management(self):
        """Carga la sección para gestionar otros administradores (solo para super-admins)."""
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
                content=ft.Column([
                    ft.Text("Administra las cuentas con acceso al panel de control.", size=16),
                    create_data_table(admin_columns, admin_rows),
                    ft.Row([
                        # ft.ElevatedButton("Añadir Admin", on_click=lambda e: show_snackbar(self.page, "Añadir admin - implementar.")),
                        # ft.ElevatedButton("Editar Admin", on_click=lambda e: show_snackbar(self.page, "Editar admin - implementar.")),
                        # ft.ElevatedButton("Eliminar Admin", on_click=lambda e: show_snackbar(self.page, "Eliminar admin - implementar.")),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
                width=800
            )
        )

# Para usar esta vista, tu main.py debería verse algo así:
# import flet as ft
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from config import Config
# from core.models import Base
# from views.main_view import MainView # Importa la vista principal también
# from views.admin_view import AdminView
#
# # Importar todos los servicios
# from services.cliente_service import ClienteService
# from services.menu_service import MenuService
# from services.pedido_service import PedidoService
# from services.financiero_service import FinancieroService
# from services.pizzeria_info_service import PizzeriaInfoService
# from services.administrador_service import AdministradorService
#
# def main(page: ft.Page):
#     # Configuración de la base de datos
#     engine = create_engine(Config.DATABASE_URL)
#     Base.metadata.create_all(engine)
#     Session = sessionmaker(bind=engine)
#
#     # Instanciar servicios
#     cliente_service = ClienteService(Session)
#     menu_service = MenuService(Session)
#     pedido_service = PedidoService(Session)
#     financiero_service = FinancieroService(Session)
#     pizzeria_info_service = PizzeriaInfoService(Session)
#     administrador_service = AdministradorService(Session)
#
#     # Crear instancias de las vistas, pasando los servicios
#     main_view_instance = MainView(page)
#     # Pasa las instancias de los servicios a AdminView
#     admin_view_instance = AdminView(page, cliente_service, menu_service, pedido_service,
#                                     financiero_service, pizzeria_info_service, administrador_service)
#
#     def view_pop(view):
#         page.views.pop()
#         top_view = page.views[-1]
#         page.go(top_view.route)
#
#     def route_change(route):
#         page.views.clear()
#         if page.route == "/":
#             page.views.append(main_view_instance)
#         elif page.route == "/admin":
#             page.views.append(admin_view_instance)
#         # Otras rutas si las tienes
#         page.update()
#
#     page.on_route_change = route_change
#     page.on_view_pop = view_pop
#     page.go(page.route) # Asegura que la ruta inicial se maneje correctamente
#
# if __name__ == "__main__":
#     ft.app(target=main)
