"""Interfaz responsiva para administrar reservas del laboratorio."""

from datetime import date, datetime

import flet as ft
import mysql.connector

import db


def main(page: ft.Page):
    """Construye la pantalla principal de la aplicación."""
    page.title = "Reservas del laboratorio"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.BLUE_GREY_50
    page.padding = 0
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    reserva_en_edicion = {"id": None}
    fecha_seleccionada = {"valor": date.today()}

    # Los campos no usan anchos fijos; ResponsiveRow decide su tamaño.
    alumno = ft.Dropdown(
        label="Alumno", hint_text="Seleccione un alumno",
        leading_icon=ft.Icons.PERSON, filled=True,
        fill_color=ft.Colors.WHITE, width=430,
        menu_style=ft.MenuStyle(fixed_size=ft.Size.from_width(430)),
        enable_search=True,
    )
    computador = ft.Dropdown(
        label="Computador", hint_text="Seleccione un equipo",
        leading_icon=ft.Icons.COMPUTER, filled=True,
        fill_color=ft.Colors.WHITE, width=320,
        menu_style=ft.MenuStyle(fixed_size=ft.Size.from_width(320)),
        enable_search=True,
    )
    bloque = ft.Dropdown(
        label="Bloque", hint_text="Seleccione un bloque",
        leading_icon=ft.Icons.SCHEDULE, filled=True,
        fill_color=ft.Colors.WHITE, width=430,
        menu_style=ft.MenuStyle(fixed_size=ft.Size.from_width(400)),
        enable_search=True,
    )
    texto_fecha = ft.Text(
        fecha_seleccionada["valor"].strftime("%d/%m/%Y"),
        size=16, weight=ft.FontWeight.BOLD,
    )
    mensaje = ft.Text(size=14, weight=ft.FontWeight.BOLD)
    lista_reservas = ft.Column(spacing=12)

    def avisar(texto, es_error=False):
        """Muestra un mensaje verde o rojo."""
        mensaje.value = texto
        mensaje.color = ft.Colors.RED_700 if es_error else ft.Colors.GREEN_700
        page.update()

    def recibir_fecha(evento):
        """Recibe y muestra la fecha seleccionada en el calendario."""
        if evento.control.value is None:
            return
        valor = evento.control.value
        if isinstance(valor, datetime):
            valor = valor.date()
        fecha_seleccionada["valor"] = valor
        texto_fecha.value = valor.strftime("%d/%m/%Y")
        page.update()

    selector_fecha = ft.DatePicker(
        value=datetime.now(), current_date=datetime.now(),
        first_date=datetime.now(), last_date=datetime(2030, 12, 31),
        help_text="Seleccione la fecha de la reserva",
        cancel_text="Cancelar", confirm_text="Aceptar",
        on_change=recibir_fecha,
    )
    boton_fecha = ft.Button(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.BLUE_700),
                texto_fecha,
                ft.Icon(ft.Icons.ARROW_DROP_DOWN, color=ft.Colors.BLUE_GREY_500),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        tooltip="Abrir calendario", width=float("inf"),
        on_click=lambda _: page.show_dialog(selector_fecha),
    )

    def cargar_selectores():
        """Carga los Dropdown con información obtenida desde MySQL."""
        alumno.options = [
            ft.DropdownOption(str(a["id"]), f'{a["nombre"]} - {a["curso"]}')
            for a in db.obtener_alumnos()
        ]
        computador.options = [
            ft.DropdownOption(str(c["id"]), c["codigo"])
            for c in db.obtener_computadores()
        ]
        bloque.options = [
            ft.DropdownOption(
                str(b["id"]), f'{b["nombre"]} ({b["inicio"]} - {b["fin"]})'
            )
            for b in db.obtener_bloques()
        ]

    def cargar_reservas():
        """Lee las reservas y las presenta en tarjetas responsivas."""
        lista_reservas.controls.clear()
        reservas = db.obtener_reservas()

        for reserva in reservas:
            datos = ft.Container(
                col={"xs": 12, "md": 9},
                content=ft.Row(
                    controls=[
                        ft.CircleAvatar(
                            content=ft.Icon(ft.Icons.COMPUTER, color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE_600,
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    f'{reserva["computador"]} · {reserva["bloque"]}',
                                    size=17, weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLUE_GREY_900,
                                ),
                                ft.Text(
                                    f'{reserva["alumno"]} · {reserva["curso"]}',
                                    color=ft.Colors.BLUE_GREY_600,
                                ),
                                ft.Text(
                                    f'Fecha: {reserva["fecha"]}',
                                    color=ft.Colors.BLUE_700,
                                ),
                            ],
                            spacing=2, expand=True,
                        ),
                    ],
                ),
            )
            acciones = ft.Container(
                col={"xs": 12, "md": 3},
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.EDIT, icon_color=ft.Colors.BLUE_700,
                            tooltip="Editar reserva",
                            on_click=lambda e, r=reserva: seleccionar_edicion(r),
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, icon_color=ft.Colors.RED_600,
                            tooltip="Eliminar reserva",
                            on_click=lambda e, rid=reserva["id"]: eliminar(rid),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            )
            lista_reservas.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=14, padding=16,
                    content=ft.ResponsiveRow(
                        controls=[datos, acciones], spacing=12, run_spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )

        if not reservas:
            lista_reservas.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
                    border_radius=14, padding=32,
                    alignment=ft.Alignment.CENTER,
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.Icons.EVENT_AVAILABLE, size=44,
                                    color=ft.Colors.BLUE_300),
                            ft.Text("Todavía no hay reservas activas.",
                                    color=ft.Colors.BLUE_GREY_600),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                )
            )

    def cambiar_fecha(valor):
        """Actualiza el calendario y el texto visible."""
        if isinstance(valor, str):
            valor = date.fromisoformat(valor)
        elif isinstance(valor, datetime):
            valor = valor.date()
        fecha_seleccionada["valor"] = valor
        texto_fecha.value = valor.strftime("%d/%m/%Y")
        selector_fecha.value = datetime.combine(valor, datetime.min.time())

    def limpiar_formulario():
        """Deja el formulario listo para agregar."""
        reserva_en_edicion["id"] = None
        alumno.value = None
        computador.value = None
        bloque.value = None
        cambiar_fecha(date.today())
        titulo_formulario.value = "Nueva reserva"
        boton_guardar.content = "Agregar reserva"
        boton_guardar.icon = ft.Icons.ADD
        boton_cancelar.visible = False

    def seleccionar_edicion(reserva):
        """Carga la reserva seleccionada en el formulario."""
        reserva_en_edicion["id"] = reserva["id"]
        alumno.value = str(reserva["alumno_id"])
        computador.value = str(reserva["computador_id"])
        bloque.value = str(reserva["bloque_id"])
        cambiar_fecha(reserva["fecha"])
        titulo_formulario.value = "Editar reserva"
        boton_guardar.content = "Guardar cambios"
        boton_guardar.icon = ft.Icons.SAVE
        boton_cancelar.visible = True
        avisar("Modifique los datos y presione Guardar cambios.")

    def cancelar_edicion(evento):
        """Cancela la edición sin modificar la base de datos."""
        limpiar_formulario()
        mensaje.value = ""
        page.update()

    def guardar_reserva(evento):
        """Agrega una reserva nueva o actualiza la seleccionada."""
        if not alumno.value or not computador.value or not bloque.value:
            avisar("Complete todos los campos.", es_error=True)
            return
        fecha_mysql = fecha_seleccionada["valor"].isoformat()

        try:
            if reserva_en_edicion["id"] is None:
                db.realizar_reserva(
                    int(alumno.value), int(computador.value),
                    int(bloque.value), fecha_mysql,
                )
                texto_exito = "Reserva agregada correctamente."
            else:
                db.actualizar_reserva(
                    reserva_en_edicion["id"], int(alumno.value),
                    int(computador.value), int(bloque.value), fecha_mysql,
                )
                texto_exito = "Reserva actualizada correctamente."
            limpiar_formulario()
            cargar_reservas()
            avisar(texto_exito)
        except mysql.connector.Error as error:
            avisar(f"No fue posible guardar: {error.msg}", es_error=True)
        except ValueError as error:
            avisar(str(error), es_error=True)

    def eliminar(reserva_id):
        """Elimina la reserva seleccionada."""
        try:
            db.eliminar_reserva(reserva_id)
            if reserva_en_edicion["id"] == reserva_id:
                limpiar_formulario()
            cargar_reservas()
            avisar("Reserva eliminada correctamente.")
        except mysql.connector.Error as error:
            avisar(f"No fue posible eliminar: {error.msg}", es_error=True)

    titulo_formulario = ft.Text(
        "Nueva reserva", size=21, weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_GREY_900,
    )
    boton_guardar = ft.Button(
        content="Agregar reserva", icon=ft.Icons.ADD,
        bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE,
        on_click=guardar_reserva,
    )
    boton_cancelar = ft.OutlinedButton(
        content="Cancelar edición", icon=ft.Icons.CLOSE,
        visible=False, on_click=cancelar_edicion,
    )

    encabezado = ft.Container(
        bgcolor=ft.Colors.BLUE_700, border_radius=18, padding=24,
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    col={"xs": 12, "sm": 2},
                    content=ft.Icon(ft.Icons.COMPUTER, size=46,
                                    color=ft.Colors.WHITE),
                ),
                ft.Container(
                    col={"xs": 12, "sm": 10},
                    content=ft.Column(
                        controls=[
                            ft.Text("Laboratorio Digital", size=28,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE),
                            ft.Text("Sistema CRUD de reserva de computadores",
                                    color=ft.Colors.BLUE_100),
                        ],
                        spacing=2,
                    ),
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )

    # 12 columnas en pantallas pequeñas y 6 en medianas o grandes.
    campos = ft.ResponsiveRow(
        controls=[
            ft.Container(content=alumno, col={"xs": 12, "md": 6}),
            ft.Container(content=computador, col={"xs": 12, "md": 6}),
            ft.Container(content=bloque, col={"xs": 12, "md": 6}),
            ft.Container(
                col={"xs": 12, "md": 6},
                content=ft.Column(
                    controls=[
                        ft.Text("Fecha de la reserva", size=12,
                                color=ft.Colors.BLUE_GREY_600),
                        boton_fecha,
                    ],
                    spacing=4,
                ),
            ),
        ],
        spacing=16, run_spacing=16,
    )

    formulario = ft.Container(
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=18, padding=24,
        content=ft.Column(
            controls=[
                titulo_formulario,
                ft.Text("Seleccione los datos. La fecha se elige desde el calendario.",
                        color=ft.Colors.BLUE_GREY_600),
                campos,
                ft.Row(controls=[boton_guardar, boton_cancelar],
                       wrap=True, spacing=10),
                mensaje,
            ],
            spacing=16,
        ),
    )

    contenido = ft.Column(
        controls=[
            encabezado,
            formulario,
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.BLUE_700),
                    ft.Text("Reservas activas", size=22,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_900),
                ]
            ),
            lista_reservas,
            ft.Text("Administración de Bases de Datos · 4° Medio",
                    size=12, color=ft.Colors.BLUE_GREY_400,
                    text_align=ft.TextAlign.CENTER),
        ],
        spacing=20,
    )


    marco = ft.Container(content=contenido, padding=24, width=1100)

    def ajustar_ancho(evento=None):
        """Mantiene el contenido centrado y proporcionado al redimensionar."""
        ancho_ventana = page.width or 1100
        marco.width = max(320, min(ancho_ventana, 1100))


        ancho_disponible = max(260, ancho_ventana - 70)
        alumno.menu_width = min(430, ancho_disponible)
        computador.menu_width = min(320, ancho_disponible)
        bloque.menu_width = min(400, ancho_disponible)

        # MenuStyle fuerza el ancho del panel gris de las opciones.
        alumno.menu_style = ft.MenuStyle(
            fixed_size=ft.Size.from_width(alumno.menu_width)
        )
        computador.menu_style = ft.MenuStyle(
            fixed_size=ft.Size.from_width(computador.menu_width)
        )
        bloque.menu_style = ft.MenuStyle(
            fixed_size=ft.Size.from_width(bloque.menu_width)
        )

        if evento is not None:
            page.update()

    page.on_resize = ajustar_ancho
    ajustar_ancho()

    try:
        cargar_selectores()
        cargar_reservas()
    except mysql.connector.Error as error:
        mensaje.value = f"Error de conexión con MySQL: {error.msg}"
        mensaje.color = ft.Colors.RED_700

    page.add(ft.SafeArea(content=marco))


if __name__ == "__main__":
    ft.run(main)
