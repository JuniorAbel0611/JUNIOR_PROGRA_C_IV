import flet as ft
import os
import sys
import subprocess

# Usuario/contraseña de ejemplo
USUARIO = "junior"
PASSWORD = "junior2002"

def main(page: ft.Page):
    if not page.web:
        page.window.width = 420
        page.window.height = 350
        page.window.center()
        page.window.resizable = False

    page.title = "Login - Sistema de Ventas"
    page.bgcolor = "#F5F7FA"  # fondo claro
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Campos de entrada
    user_input = ft.TextField(label="Usuario", width=250)
    pass_input = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=250)
    mensaje = ft.Text("", color="red")

    # Función para abrir dashboard
    def abrir_dashboard():
        page.window.close()
        ruta_dashboard = os.path.join(os.path.dirname(__file__), "dashboard.py")
        subprocess.Popen([sys.executable, ruta_dashboard])

    # Función para validar login
    def validar_login(e):
        if user_input.value == USUARIO and pass_input.value == PASSWORD:
            mensaje.value = "✅ Acceso correcto"
            page.update()
            abrir_dashboard()
        else:
            mensaje.value = "❌ Usuario o contraseña incorrectos"
            page.update()

    # Botón de login
    btn_login = ft.ElevatedButton(
        text="Ingresar",
        bgcolor="#2196F3",
        color="white",
        width=250,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=validar_login
    )

    # Tarjeta central
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
