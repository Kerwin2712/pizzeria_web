# utils/widgets.py
import flet as ft
from datetime import datetime, date, time

class CustomCard(ft.Card):
    """
    Una tarjeta personalizada con título y contenido.
    """
    def __init__(self, title: str, content: ft.Control, width: float = None, height: float = None, bgcolor: str = None, title_color: str = ft.colors.BLACK):
        super().__init__(
            elevation=10,
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=title_color), # Color del título
                        ft.Divider(),
                        content,
                    ],
                    spacing=10,
                ),
                padding=20,
                width=width,
                height=height,
                border_radius=ft.border_radius.all(15), # Bordes redondeados
                bgcolor=bgcolor # Añadido bgcolor aquí para el contenido de la tarjeta
            )
        )

def create_data_table(columns: list[str], rows_data: list[list[str]],
                      heading_row_bgcolor: str = ft.colors.BLUE_GREY_100,
                      data_row_bgcolor_hover: str = ft.colors.BLUE_GREY_50,
                      border_color: str = ft.colors.BLUE_GREY_200,
                      text_color: str = ft.colors.BLACK): # Nuevo: color de texto para celdas
    """
    Crea una tabla de datos de Flet.

    Args:
        columns (list[str]): Nombres de las columnas.
        rows_data (list[list[str]]): Datos de las filas. Cada lista interna es una fila.
        heading_row_bgcolor (str, optional): Color de fondo de la fila de encabezado. Defaults to ft.colors.BLUE_GREY_100.
        data_row_bgcolor_hover (str, optional): Color de fondo de las filas al pasar el ratón. Defaults to ft.colors.BLUE_GREY_50.
        border_color (str, optional): Color del borde de la tabla. Defaults to ft.colors.BLUE_GREY_200.
        text_color (str, optional): Color del texto de las celdas y encabezados. Defaults to ft.colors.BLACK.

    Returns:
        ft.DataTable: La tabla de datos de Flet.
    """
    data_columns = [ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD, color=text_color)) for col in columns]
    data_rows = []
    for row in rows_data:
        cells = [ft.DataCell(ft.Text(str(cell), color=text_color)) for cell in row]
        data_rows.append(ft.DataRow(cells=cells))

    return ft.DataTable(
        columns=data_columns,
        rows=data_rows,
        heading_row_color=heading_row_bgcolor,
        data_row_color={"hovered": data_row_bgcolor_hover},
        show_bottom_border=True,
        border_radius=ft.border_radius.all(8), # Bordes redondeados
        border=ft.border.all(1, border_color)
    )

def create_date_picker(page: ft.Page, on_change_callback):
    """
    Crea un selector de fecha de Flet (calendario).

    Args:
        page (ft.Page): La página de Flet a la que se añadirá el DatePicker.
        on_change_callback (function): Función a llamar cuando la fecha cambie.
                                       Recibe un evento con DatePicker.value.
    Returns:
        ft.DatePicker: El control DatePicker.
    """
    date_picker = ft.DatePicker(
        first_date=datetime(2023, 1, 1),
        last_date=datetime(2026, 12, 31),
        on_change=on_change_callback,
    )
    page.overlay.append(date_picker) # Es importante añadirlo al overlay de la página
    return date_picker

def create_time_picker(page: ft.Page, on_change_callback):
    """
    Crea un selector de hora de Flet.

    Args:
        page (ft.Page): La página de Flet a la que se añadirá el TimePicker.
        on_change_callback (function): Función a llamar cuando la hora cambie.
                                       Recibe un evento con TimePicker.value.
    Returns:
        ft.TimePicker: El control TimePicker.
    """
    time_picker = ft.TimePicker(
        on_change=on_change_callback,
        initial_time=ft.Time(hour=datetime.now().hour, minute=datetime.now().minute),
    )
    page.overlay.append(time_picker) # Es importante añadirlo al overlay de la página
    return time_picker


def show_snackbar(page: ft.Page, message: str, color: str = ft.colors.GREEN_500, icon: ft.Icon = None):
    """
    Muestra una notificación tipo SnackBar en la parte inferior de la pantalla.

    Args:
        page (ft.Page): La página de Flet.
        message (str): El mensaje a mostrar.
        color (str, optional): Color de fondo del SnackBar. Defaults to ft.colors.GREEN_500.
        icon (ft.Icon, optional): Icono opcional a mostrar. Defaults to None.
    """
    page.snack_bar = ft.SnackBar(
        ft.Row([
            icon if icon else ft.Icon(ft.icons.INFO),
            ft.Text(message, color=ft.colors.WHITE)
        ], alignment=ft.MainAxisAlignment.START),
        open=True,
        bgcolor=color,
        duration=3000, # 3 segundos
        show_close_button=True,
        action="Cerrar",
        padding=15,
        margin=10,
        shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(10)) # Bordes redondeados
    )
    page.snack_bar.open = True
    page.update()

def show_alert_dialog(page: ft.Page, title: str, content: str, on_close: callable = None, title_color: str = ft.colors.BLACK, content_color: str = ft.colors.BLACK):
    """
    Muestra un diálogo de alerta modal.

    Args:
        page (ft.Page): La página de Flet.
        title (str): Título del diálogo.
        content (str): Contenido del mensaje.
        on_close (callable, optional): Función a llamar al cerrar el diálogo.
        title_color (str, optional): Color del texto del título. Defaults to ft.colors.BLACK.
        content_color (str, optional): Color del texto del contenido. Defaults to ft.colors.BLACK.
    """
    def close_dlg(e):
        dialog.open = False
        page.update()
        if on_close:
            on_close()

    dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text(title, color=title_color),
        content=ft.Text(content, color=content_color),
        actions=[
            ft.TextButton("Aceptar", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        shape=ft.RoundedRectangleBorder(radius=ft.border_radius.all(15)) # Bordes redondeados
    )
    page.dialog = dialog
    dialog.open = True
    page.update()

def create_message_box(message: str, title: str = "Mensaje", icon: ft.Icon = None, bgcolor: str = ft.colors.BLUE_GREY_50, text_color: str = ft.colors.BLACK):
    """
    Crea un simple contenedor de mensaje.

    Args:
        message (str): El texto del mensaje.
        title (str, optional): Título opcional del mensaje. Defaults to "Mensaje".
        icon (ft.Icon, optional): Icono opcional para el mensaje. Defaults to None.
        bgcolor (str, optional): Color de fondo del contenedor. Defaults to ft.colors.BLUE_GREY_50.
        text_color (str, optional): Color del texto dentro del mensaje. Defaults to ft.colors.BLACK.

    Returns:
        ft.Container: Un contenedor con el mensaje.
    """
    return ft.Container(
        content=ft.Column(
            [
                ft.Row([
                    icon if icon else ft.Icon(ft.icons.MESSAGE, color=text_color),
                    ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=text_color)
                ], alignment=ft.MainAxisAlignment.START, spacing=10),
                ft.Divider(),
                ft.Text(message, size=16, color=text_color),
            ]
        ),
        padding=15,
        margin=10,
        bgcolor=bgcolor, # Usar el bgcolor pasado
        border_radius=ft.border_radius.all(10), # Bordes redondeados
        border=ft.border.all(1, ft.colors.BLUE_GREY_700) # Ajustado para modo oscuro
    )

def create_simple_bar_chart(data_points: dict, title: str = "Gráfico", text_color: str = ft.colors.BLACK, bar_color: str = ft.colors.BLUE_500, card_bgcolor: str = None, title_color: str = ft.colors.BLACK):
    """
    Crea un gráfico de barras simple usando Canvas de Flet.
    Ideal para mostrar totales de ingresos/gastos por período.

    Args:
        data_points (dict): Un diccionario donde las claves son etiquetas (ej. meses)
                            y los valores son los números a graficar.
                            Ej: {"Ene": 1000, "Feb": 1200, "Mar": 900}
        title (str, optional): Título del gráfico. Defaults to "Gráfico".
        text_color (str, optional): Color del texto en el gráfico. Defaults to ft.colors.BLACK.
        bar_color (str, optional): Color de las barras del gráfico. Defaults to ft.colors.BLUE_500.
        card_bgcolor (str, optional): Color de fondo de la tarjeta que contiene el gráfico. Defaults to None.
        title_color (str, optional): Color del título de la tarjeta del gráfico. Defaults to ft.colors.BLACK.

    Returns:
        ft.Container: Un contenedor con el gráfico de barras.
    """
    if not data_points:
        return create_message_box("No hay datos para mostrar el gráfico.", icon=ft.icons.BAR_CHART, bgcolor=card_bgcolor, text_color=text_color)

    labels = list(data_points.keys())
    values = list(data_points.values())

    max_value = max(values) if values else 1
    if max_value == 0:
        max_value = 1

    chart_elements = []
    bar_width_factor = 0.6

    total_bar_area_width = 400 - 40
    bar_spacing = 10
    num_bars = len(labels)
    bar_width = (total_bar_area_width - (num_bars - 1) * bar_spacing) / num_bars

    if bar_width <= 0:
        bar_width = 20

    for i, (label, value) in enumerate(data_points.items()):
        bar_height = (value / max_value) * 150

        x_pos = 20 + i * (bar_width + bar_spacing)

        chart_elements.append(
            ft.Container(
                content=ft.Column([
                    ft.Text(f"${value:,.2f}", size=12, weight=ft.FontWeight.BOLD, color=text_color),
                    ft.Container(
                        width=bar_width * bar_width_factor,
                        height=bar_height,
                        bgcolor=bar_color,
                        border_radius=ft.border_radius.all(5)
                    ),
                    ft.Text(label, size=12, color=text_color),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=5),
                alignment=ft.alignment.bottom_center,
                left=x_pos,
                bottom=0,
            )
        )

    return CustomCard(
        title=title,
        content=ft.Container(
            content=ft.Stack(
                chart_elements,
                width=400,
                height=200,
            ),
            alignment=ft.alignment.center,
            expand=True
        ),
        width=450,
        height=300,
        bgcolor=card_bgcolor, # Pasa el color de fondo a la tarjeta
        title_color=title_color # Pasa el color del título
    )

