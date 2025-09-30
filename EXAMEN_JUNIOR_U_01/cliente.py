import flet as ft
import threading
import time
import subprocess, sys, os

boletos = 3
lock = threading.Lock()

def main(page: ft.Page):
    global boletos
    page.title = "Cliente - Reservas Tour"

    estado = ft.Text(f"Boletos disponibles: {boletos}")
    mensaje = ft.Text("")

    def reservar_viaje(e):
        def hilo_reserva():
            global boletos
            mensaje.value = "Reservando..."
            page.update()
            
            time.sleep(1)  
            
            with lock:
                if boletos > 0:
                    boletos -= 1
                    mensaje.value = "✅ Reservado"
                else:
                    mensaje.value = "❌ No hay cupos disponibles"
            
            estado.value = f"Boletos disponibles: {boletos}"
            page.update()
        
        threading.Thread(target=hilo_reserva).start()

    def logout(e):
        ruta = os.path.join(os.path.dirname(__file__), "main.py")
        subprocess.Popen([sys.executable, ruta])
        page.window.close()

    page.add(
        ft.Column(
            [
                ft.Text("🧳 Tour Guiado - Reserva tu viaje", size=20),
                estado,
                ft.ElevatedButton("Reservar viaje", on_click=reservar_viaje),
                mensaje,
                ft.ElevatedButton("🚪 Logout", on_click=logout)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
