import flet as ft

def main(page: ft.Page):
    page.title = "Segunda clase, programación concurrente"
    page.add(ft.Text("Welcome to flet!"))

ft.app(target=main)