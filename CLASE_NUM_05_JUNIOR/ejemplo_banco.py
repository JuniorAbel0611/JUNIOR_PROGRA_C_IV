import threading
import time

# Recurso compartido
boletos = 3
lock = threading.Lock()

def comprar_boleto(nombre):
    global boletos
    for i in range(2):  # Cada hilo intentará comprar 2 veces
        print(f"[{nombre}] Intentando comprar un boleto (operación {i+1})...")
        
        with lock:  # Bloqueo acceso a la sección crítica
            print(f"[{nombre}] 🔒 Entró a la sección crítica.")
            
            if boletos > 0:
                print(f"[{nombre}] 🎟️ Comprando un boleto...")
                time.sleep(1)  # Simula el tiempo de compra
                boletos -= 1
                print(f"[{nombre}] ✅ Operación finalizada. Boletos restantes: {boletos}")
            else:
                print(f"[{nombre}] ❌ No se pudo comprar. Ya no quedan boletos ({boletos}).")
            
            print(f"[{nombre}] 🔓 Saliendo de la sección crítica.\n")
        
        time.sleep(0.5)  # Pausa para alternar entre hilos

# Crear hilos
hilos = []
for i in range(4):  # 4 hilos
    hilo = threading.Thread(target=comprar_boleto, args=(f"Hilo {i+1}",))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos finalicen
for h in hilos:
    h.join()

print(f"✅ Todas las operaciones han finalizado. Boletos restantes: {boletos}")
