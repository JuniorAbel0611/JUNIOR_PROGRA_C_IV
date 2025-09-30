import flet as ft, os, sys, subprocess

def main(page: ft.Page):
    page.title = "Administrador"

    def boton_logout(e):
        subprocess.Popen([sys.executable, "main.py"])  # vuelve al login
        page.window.close()

    page.add(
        ft.Column(
            [
                ft.Text("🛠 Bienvenido ADMINISTRADOR"),
                ft.ElevatedButton("cerrar", on_click=boton_logout)
            ]
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
