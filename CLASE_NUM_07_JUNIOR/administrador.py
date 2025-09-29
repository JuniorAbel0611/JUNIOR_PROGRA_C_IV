import flet as ft

def main(page: ft.Page):
    if not page.web:
        page.window.width = 600
        page.window.height = 400
        page.window.center()
        page.window.resizable = True

    page.title = "Panel de Administrador"
    page.bgcolor = "#E3F2FD"

    page.add(
        ft.Column(
            [
                ft.Text("👨‍💼 Bienvenido Administrador", size=24, weight=ft.FontWeight.BOLD, color="blue"),
                ft.Text("Aquí puedes gestionar usuarios, productos y ventas."),
                ft.ElevatedButton(text="Cerrar", on_click=lambda e: page.window.close())
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
