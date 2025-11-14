import flet as ft
from conexion import ConexionDB


class PeliculasView(ft.Container):
    def __init__(self, page, volver_atras):
        super().__init__(expand=True)
        self.page = page
        self.volver_atras = volver_atras
        self.conexion = ConexionDB()

        self.titulo = ft.Text("🎬 Gestión de Películas", size=22, weight="bold")

        # --- Tabla principal ---
        self.tabla = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Título")),
                ft.DataColumn(ft.Text("Director")),
                ft.DataColumn(ft.Text("Género")),
                ft.DataColumn(ft.Text("Año estreno")),
                ft.DataColumn(ft.Text("Duración")),
                ft.DataColumn(ft.Text("Clasificación")),
                ft.DataColumn(ft.Text("País")),
                ft.DataColumn(ft.Text("Idioma")),
                ft.DataColumn(ft.Text("Acciones")),
            ],
            rows=[],
        )

        # --- Botones superiores ---
        self.btn_volver = ft.ElevatedButton("⬅️ Volver", on_click=lambda e: self.volver_atras())
        self.btn_actualizar = ft.ElevatedButton("🔄 Actualizar", on_click=lambda e: self.cargar_peliculas())
        self.btn_agregar = ft.ElevatedButton("➕ Agregar", on_click=lambda e: self.mostrar_formulario_nuevo())

        # --- Contenedor principal ---
        self.content = ft.Column(
            [
                self.titulo,
                ft.Row(
                    [self.btn_volver, self.btn_actualizar, self.btn_agregar],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(
                    self.tabla,
                    expand=True,
                    border_radius=10,
                    padding=10,
                    bgcolor=ft.Colors.BLUE_50,
                ),
            ],
            spacing=15,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )

        # --- Agregar contenido al contenedor principal ---
        self.controls = [self.content]

        # --- Cargar datos iniciales ---
        self.cargar_peliculas()

    # =============================
    #   CARGAR PELÍCULAS
    # =============================
    def cargar_peliculas(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT id_pelicula, titulo, director, genero, year_estreno, duracion, 
                           clasificacion, pais_origen, idioma 
                    FROM pelicula
                """)
                resultados = cur.fetchall()

                self.tabla.rows.clear()
                for fila in resultados:
                    id_pelicula = fila[0]

                    # Crear botones de acción
                    def crear_botones(pid):
                        return ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, _pid=pid: self.mostrar_formulario_editar(_pid),
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    tooltip="Eliminar",
                                    icon_color="red",
                                    on_click=lambda e, _pid=pid: self.eliminar_pelicula(_pid),
                                ),
                            ]
                        )

                    self.tabla.rows.append(
                        ft.DataRow(
                            cells=[
                                ft.DataCell(ft.Text(str(fila[0]))),
                                ft.DataCell(ft.Text(fila[1] or "")),
                                ft.DataCell(ft.Text(fila[2] or "")),
                                ft.DataCell(ft.Text(fila[3] or "")),
                                ft.DataCell(ft.Text(str(fila[4]) or "")),
                                ft.DataCell(ft.Text(str(fila[5]) or "")),
                                ft.DataCell(ft.Text(fila[6] or "")),
                                ft.DataCell(ft.Text(fila[7] or "")),
                                ft.DataCell(ft.Text(fila[8] or "")),
                                ft.DataCell(crear_botones(id_pelicula)),
                            ]
                        )
                    )

                self.page.update()
            except Exception as e:
                print(f"❌ Error al cargar películas: {e}")
            finally:
                self.conexion.cerrar(conexion)
        else:
            print("⚠️ No se pudo conectar a la base de datos.")

    # =============================
    #   FORMULARIO NUEVA PELÍCULA
    # =============================
    def mostrar_formulario_nuevo(self):
        txt_titulo = ft.TextField(label="Título")
        txt_director = ft.TextField(label="Director")
        txt_genero = ft.TextField(label="Género")
        txt_year = ft.TextField(label="Año estreno")
        txt_duracion = ft.TextField(label="Duración")
        txt_clasificacion = ft.TextField(label="Clasificación")
        txt_pais = ft.TextField(label="País de origen")
        txt_idioma = ft.TextField(label="Idioma")

        def guardar_nueva(e):
            conexion = self.conexion.conectar()
            if conexion:
                cur = conexion.cursor()
                try:
                    cur.execute("""
                        INSERT INTO pelicula 
                        (titulo, director, genero, year_estreno, duracion, clasificacion, pais_origen, idioma, fecha_registro)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    """, (
                        txt_titulo.value, txt_director.value, txt_genero.value,
                        txt_year.value, txt_duracion.value, txt_clasificacion.value,
                        txt_pais.value, txt_idioma.value
                    ))
                    conexion.commit()
                    self.cerrar_dialogo(dlg)
                    self.cargar_peliculas()
                    self.page.snack_bar = ft.SnackBar(
                        content=ft.Text("Película agregada correctamente ✅", color="white"),
                        bgcolor="green",
                        open=True
                    )
                    self.page.update()
                except Exception as ex:
                    print(f"❌ Error al insertar película: {ex}")
                finally:
                    self.conexion.cerrar(conexion)

        dlg = ft.AlertDialog(
            title=ft.Text("➕ Nueva Película"),
            content=ft.Column(
                [txt_titulo, txt_director, txt_genero, txt_year,
                 txt_duracion, txt_clasificacion, txt_pais, txt_idioma],
                spacing=10
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg)),
                ft.TextButton("Guardar", on_click=guardar_nueva),
            ],
        )
        self.page.dialog = dlg
        self.page.dialog.open = True
        self.page.update()

    # =============================
    #   FORMULARIO EDITAR PELÍCULA
    # =============================
    def mostrar_formulario_editar(self, pelicula_id):
        print(f"🧩 Abriendo edición para película {pelicula_id}")
        from acciones.editar_pelicula_view import EditarPeliculaView
        editar_vista = EditarPeliculaView(self.page, pelicula_id)
        self.page.clean()
        self.page.add(editar_vista)
        self.page.update()

    # =============================
    #   ELIMINAR PELÍCULA
    # =============================
    def eliminar_pelicula(self, pelicula_id):
        dlg_confirm = ft.AlertDialog(
            title=ft.Text("⚠️ Confirmar eliminación"),
            content=ft.Text("¿Está seguro de que desea eliminar esta película?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: self.cerrar_dialogo(dlg_confirm)),
                ft.TextButton(
                    "Eliminar",
                    style=ft.ButtonStyle(color="white", bgcolor="red"),
                    on_click=lambda e: self.confirmar_eliminar(pelicula_id, dlg_confirm),
                ),
            ],
        )
        self.page.dialog = dlg_confirm
        self.page.dialog.open = True
        self.page.update()

    def confirmar_eliminar(self, pelicula_id, dlg_confirm):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("DELETE FROM pelicula WHERE id_pelicula = %s", (pelicula_id,))
                conexion.commit()
                self.cerrar_dialogo(dlg_confirm)
                self.cargar_peliculas()
                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Película eliminada correctamente 🗑️", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()
            except Exception as e:
                print(f"❌ Error al eliminar película: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # =============================
    #   CERRAR DIÁLOGO
    # =============================
    def cerrar_dialogo(self, dlg):
        dlg.open = False
        self.page.update()
