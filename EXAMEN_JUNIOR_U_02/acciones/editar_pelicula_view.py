import flet as ft
from conexion import ConexionDB

class EditarPeliculaView(ft.Container):
    def __init__(self, page, pelicula_id):
        super().__init__(expand=True)
        self.page = page
        self.pelicula_id = pelicula_id
        self.conexion = ConexionDB()

        # 🔹 Título
        self.titulo = ft.Text(f"✏️ Editar Película (ID: {pelicula_id})", size=22, weight="bold")

        # Contenido mientras carga
        self.column = ft.Column(
            [
                self.titulo,
                ft.ProgressRing(),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Contenedor principal centrado
        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,
            padding=20
        )

        self.controls = [self.content]
        self.cargar_datos_pelicula()

    # ───────────────────────────────
    def cargar_datos_pelicula(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT titulo, director, genero, year_estreno, duracion,
                           clasificacion, pais_origen, idioma
                    FROM pelicula
                    WHERE id_pelicula = %s
                """, (self.pelicula_id,))
                datos = cur.fetchone()

                if datos:
                    (titulo, director, genero, year_estreno, duracion,
                     clasificacion, pais_origen, idioma) = datos

                    # Campos editables
                    self.txt_titulo = ft.TextField(label="Título", value=titulo, width=350)
                    self.txt_director = ft.TextField(label="Director", value=director, width=350)
                    self.txt_genero = ft.TextField(label="Género", value=genero, width=350)
                    self.txt_year = ft.TextField(label="Año de estreno", value=str(year_estreno), width=350)
                    self.txt_duracion = ft.TextField(label="Duración", value=str(duracion), width=350)
                    self.txt_clasificacion = ft.TextField(label="Clasificación", value=clasificacion, width=350)
                    self.txt_pais = ft.TextField(label="País de origen", value=pais_origen, width=350)
                    self.txt_idioma = ft.TextField(label="Idioma", value=idioma, width=350)

                    # Botones
                    btn_guardar = ft.ElevatedButton(
                        "💾 Guardar cambios",
                        bgcolor=ft.Colors.GREEN,
                        color="white",
                        on_click=self.guardar_cambios
                    )
                    btn_atras = ft.OutlinedButton("⬅️ Volver", on_click=self.volver_a_peliculas)

                    # Reemplaza el contenido
                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column(
                            [
                                self.txt_titulo,
                                self.txt_director,
                                self.txt_genero,
                                self.txt_year,
                                self.txt_duracion,
                                self.txt_clasificacion,
                                self.txt_pais,
                                self.txt_idioma,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER
                        ),
                        ft.Row([btn_guardar, btn_atras], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontró la película.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar película: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE pelicula
                    SET titulo=%s, director=%s, genero=%s, year_estreno=%s,
                        duracion=%s, clasificacion=%s, pais_origen=%s, idioma=%s
                    WHERE id_pelicula=%s
                """, (
                    self.txt_titulo.value,
                    self.txt_director.value,
                    self.txt_genero.value,
                    self.txt_year.value,
                    self.txt_duracion.value,
                    self.txt_clasificacion.value,
                    self.txt_pais.value,
                    self.txt_idioma.value,
                    self.pelicula_id
                ))
                conexion.commit()
                print(f"✅ Película actualizada correctamente (ID: {self.pelicula_id})")

                self.page.snack_bar = ft.SnackBar(
                    content=ft.Text("Cambios guardados correctamente ✅", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()
                self.volver_a_peliculas()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def volver_a_peliculas(self, e=None):
        """Regresa a la vista principal de películas."""
        print("🔙 Volviendo a la vista de películas...")
        from pelicula.pelicula_view import PeliculasView
        self.page.clean()
        self.page.add(PeliculasView(self.page, None))
        self.page.update()
