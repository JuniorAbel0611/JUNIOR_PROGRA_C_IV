import flet as ft
import os
import sys
import subprocess

# Diccionario de usuarios con roles
USUARIOS = {
    "admin": {"password": "admin123", "rol": "administrador"},
    "usuario": {"password": "usuario123", "rol": "usuario"}
}

def main(page: ft.Page):
    if not page.web:
        page.window.width = 500
        page.window.height = 400
        page.window.center()
        page.window.resizable = False

    page.title = "Login - Sistema de Ventas"
    page.bgcolor = "#F5F7FA"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # --- LOGIN ---
    user_input = ft.TextField(label="Usuario", width=250)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    mensaje = ft.Text("", color="red")

    def abrir_vista(nombre_archivo):
        """Abrir el archivo correspondiente (administrador.py o usuario.py)."""
        ruta = os.path.abspath(nombre_archivo)
        subprocess.Popen([sys.executable, ruta])

        # Cerrar ventana del login SOLO después de lanzar el nuevo proceso
        if not page.web:
            page.window.close()

    # Validar login
    def validar_login(e):
        usuario = user_input.value
        clave = pass_input.value

        if usuario in USUARIOS and USUARIOS[usuario]["password"] == clave:
            rol = USUARIOS[usuario]["rol"]

            if rol == "administrador":
                abrir_vista("administrador.py")
            elif rol == "usuario":
                abrir_vista("usuario.py")
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    btn_login = ft.ElevatedButton(
        text="Ingresar",
        width=250,
        style=ft.ButtonStyle(
            bgcolor={"": "#2196F3"},
            color={"": "white"},
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=validar_login
    )

    # Tarjeta central (login)
    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("🔑 INICIAR SESIÓN", size=24, weight=ft.FontWeight.BOLD, color="#2196F3"),
                user_input,
                pass_input,
                btn_login,
                mensaje
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=20,
        border_radius=15,
        bgcolor="white",
        shadow=ft.BoxShadow(blur_radius=8, spread_radius=2, color="#B0BEC5")
    )

    page.add(card)

if __name__ == "__main__":
    ft.app(target=main)
