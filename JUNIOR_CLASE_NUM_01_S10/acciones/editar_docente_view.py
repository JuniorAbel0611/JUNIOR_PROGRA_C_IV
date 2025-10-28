import flet as ft
from conexion import ConexionDB

class EditarDocenteView(ft.Container):
    def __init__(self, page, docente_id):
        super().__init__(expand=True)
        self.page = page
        self.docente_id = docente_id
        self.conexion = ConexionDB()

        self.titulo = ft.Text(f"✏️ Editar Persona (ID: {docente_id})", size=22, weight="bold")

        # Contenido temporal mientras carga
        self.column = ft.Column(
            [
                self.titulo,
                ft.ProgressRing(),
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        self.content = ft.Container(
            content=self.column,
            alignment=ft.alignment.center,
            padding=20
        )

        self.cargar_datos_persona()

    # ───────────────────────────────
    def cargar_datos_persona(self):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    SELECT nombres, apellidos, numero_documento, telefono
                    FROM personas
                    WHERE docente_id = %s
                """, (self.docente_id,))
                datos = cur.fetchone()

                if datos:
                    nombres, apellidos, numero_documento, telefono = datos

                    # Campos dinámicos
                    self.txt_nombre = ft.TextField(label="Nombres", value=nombres, width=350)
                    self.txt_apellido = ft.TextField(label="Apellidos", value=apellidos, width=350)
                    self.txt_dni = ft.TextField(label="DNI", value=numero_documento, width=350)
                    self.txt_telefono = ft.TextField(label="Teléfono", value=telefono, width=350)

                    btn_guardar = ft.ElevatedButton(
                        "💾 Guardar cambios",
                        bgcolor=ft.Colors.GREEN,
                        color="white",
                        on_click=self.guardar_cambios
                    )

                    btn_atras = ft.OutlinedButton(
                        "⬅️ Volver a lista",
                        on_click=self.volver_a_personas
                    )

                    # Actualizamos el contenido
                    self.column.controls.clear()
                    self.column.controls.extend([
                        self.titulo,
                        ft.Column(
                            [self.txt_nombre, self.txt_apellido, self.txt_dni, self.txt_telefono],
                            spacing=10
                        ),
                        ft.Row([btn_guardar, btn_atras], spacing=15)
                    ])
                    self.page.update()
                else:
                    self.column.controls.clear()
                    self.column.controls.append(ft.Text("❌ No se encontraron datos para esta persona.", color="red"))
                    self.page.update()

            except Exception as e:
                print(f"❌ Error al cargar persona: {e}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def guardar_cambios(self, e):
        conexion = self.conexion.conectar()
        if conexion:
            cur = conexion.cursor()
            try:
                cur.execute("""
                    UPDATE personas
                    SET nombres=%s, apellidos=%s, numero_documento=%s, telefono=%s
                    WHERE docente_id=%s
                """, (
                    self.txt_nombre.value,
                    self.txt_apellido.value,
                    self.txt_dni.value,
                    self.txt_telefono.value,
                    self.docente_id
                ))
                conexion.commit()

                print(f"✅ Persona actualizada correctamente (ID: {self.docente_id})")

                self.page.snack_bar = ft.SnackBar(
                    ft.Text("Cambios guardados correctamente ✅", color="white"),
                    bgcolor="green",
                    open=True
                )
                self.page.update()

                # Volvemos a la lista automáticamente después de guardar
                self.volver_a_personas()

            except Exception as ex:
                print(f"❌ Error al guardar cambios: {ex}")
            finally:
                self.conexion.cerrar(conexion)

    # ───────────────────────────────
    def volver_a_docentes(self, e=None):
        """Regresa a la vista de Personas."""
        print("🔙 Volviendo a la vista de Personas...")
        from Docente.docentes_view import DocentesView
        self.page.clean()
        self.page.add(DocentesView(self.page, None))
        self.page.update()