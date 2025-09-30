import flet as ft

USUARIOS = {
    "admin": {"password": "admin123", "rol": "Administrador"},
    "usuario": {"password": "usuario123", "rol": "Usuario"},
    "visit": {"password": "visit123", "rol": "Visitante"},
    "cliente": {"password": "cliente123", "rol": "Cliente"}
}

def main(page: ft.Page):
    def login_view():
        page.clean()
        u = ft.TextField(label="Usuario", width=220)
        p = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=220)
        msg = ft.Text()

        def validar(e):
            if u.value in USUARIOS and USUARIOS[u.value]["password"] == p.value:
                rol_view(USUARIOS[u.value]["rol"])
            else:
                msg.value = "Datos incorrectos"; page.update()

        page.add(u, p, ft.ElevatedButton("Ingresar", on_click=validar), msg)

    def rol_view(rol):
        page.clean()
        def logout(e): login_view()
        page.add(ft.Text(f"Bienvenido {rol}"), ft.ElevatedButton("Logout", on_click=logout))

    login_view()

if __name__ == "__main__":
    ft.app(target=main)
