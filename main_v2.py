import json
import os

# --- ZONA DE FUNCIONES (Tus Herramientas) ---

def guardar_datos(lista_pedidos):
    """Guarda la lista de pedidos en un archivo .json"""
    with open("base_datos_pedidos.json", "w") as archivo:
        json.dump(lista_pedidos, archivo, indent=4)
    print("\n✅ Datos guardados en 'base_datos_pedidos.json'")

def cargar_datos():
    """Lee el archivo JSON. Si no existe, devuelve una lista vacía."""
    if os.path.exists("base_datos_pedidos.json"):
        with open("base_datos_pedidos.json", "r") as archivo:
            return json.load(archivo)
    return []

def calcular_pago_booster(pago_base, win_rate, nivel_honor):
    pago_final = pago_base
    if win_rate < 50:
        pago_final = pago_final * 0.75
        print("⚠️ Penalización aplicada: WR < 50% (-25%)")
    if nivel_honor <= 1:
        pago_final = pago_final * 0.50
        print("⚠️ Penalización aplicada: Honor 0 o 1 (-50%)")
    return pago_final

def pedir_si_no(mensaje):
    while True:
        respuesta = input(mensaje).lower()
        if respuesta == "s": return True
        if respuesta == "n": return False
        print("❌ Opción no válida. Escribe 's' o 'n'.")

def pedir_numero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("❌ ¡Error! Ingresa solo números.")

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_reporte(lista_pedidos):
    print("\n" + "="*40)
    print("📊 REPORTE HISTÓRICO DE ELO-BOOST 📊")
    print("="*40)
    total_caja = 0
    for p in lista_pedidos:
        print(f"[{p['estado']}] {p['cuenta']} | Profit: ${p['ganancia']}")
        if p['estado'] == "Terminado":
            total_caja += p['ganancia']
    print("-" * 40)
    print(f"💰 GANANCIA TOTAL EN CAJA: ${total_caja}")
    print("=" * 40)

# --- ZONA PRINCIPAL ---

# 1. Cargamos datos al iniciar
pedidos = cargar_datos()

while True:
    limpiar_pantalla()
    print("--- NUEVO PEDIDO ---")
    
    # 2. Pedir Datos
    cuenta = input("Nombre de Cuenta: ")
    booster = input("Nombre del Booster: ")
    precio_cliente = pedir_numero("Cobro al Cliente ($): ")
    pago_base = pedir_numero("Pago base acordado al Booster ($): ")
    wr_final = pedir_numero("Win Rate final de la cuenta (%): ")
    honor_final = pedir_numero("Nivel de Honor final (0-5): ")
    
    # 3. Procesar
    pago_real = calcular_pago_booster(pago_base, wr_final, honor_final)
    profit = precio_cliente - pago_real 
    es_terminado = pedir_si_no("¿El pedido ya está terminado? (s/n): ")
    estado_texto = "Terminado" if es_terminado else "Pendiente"

    # 4. Guardar en memoria
    nuevo_ticket = {
        "cuenta": cuenta,
        "booster": booster,
        "pago_booster": pago_real,
        "ganancia": profit,
        "estado": estado_texto
    }
    pedidos.append(nuevo_ticket)

    print(f"\n✅ Ticket registrado. Profit: ${profit}")
        
    # 5. Salir o Seguir
    if not pedir_si_no("\n¿Agregar otro pedido? (s/n): "):
        break

# --- FINALIZACIÓN ---
limpiar_pantalla()
mostrar_reporte(pedidos)
guardar_datos(pedidos) # Aquí se graban todos los nuevos y viejos