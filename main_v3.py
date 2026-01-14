import json
import os

# --- ZONA DE FUNCIONES ---

def buscar_pedido(lista_pedidos):
    nombre = input("\n🔍 Ingresa el nombre de la cuenta a buscar: ")
    encontrado = False
    for p in lista_pedidos:
        # Usamos .lower() para que encuentre "Cuenta" aunque escribas "cuenta"
        if p['cuenta'].lower() == nombre.lower():
            print(f"\n✅ ENCONTRADO: {p['cuenta']} | Booster: {p['booster']} | Profit: ${p['ganancia']} | Estado: {p['estado']}")
            encontrado = True
    if not encontrado:
        print("❌ No se encontró ninguna cuenta con ese nombre.")
    input("\nPresiona Enter para volver al menú...")

def actualizar_estado(lista_pedidos):
    nombre = input("\n📝 Nombre de la cuenta para cambiar a 'Terminado': ")
    for p in lista_pedidos:
        if p['cuenta'].lower() == nombre.lower():
            if p['estado'] == "Terminado":
                print("⚠️ Este pedido ya figura como Terminado.")
            else:
                p['estado'] = "Terminado"
                print(f"✅ ¡Estado actualizado! {p['cuenta']} ahora está Terminado.")
            return # Salimos de la función al encontrarlo
    print("❌ No se encontró la cuenta.")

def guardar_datos(lista_pedidos):
    with open("base_datos_pedidos.json", "w") as archivo:
        json.dump(lista_pedidos, archivo, indent=4)
    print("\n✅ Base de datos actualizada.")

def cargar_datos():
    if os.path.exists("base_datos_pedidos.json"):
        with open("base_datos_pedidos.json", "r") as archivo:
            return json.load(archivo)
    return []

def calcular_pago_booster(pago_base, win_rate, nivel_honor):
    pago_final = pago_base
    if win_rate < 50:
        pago_final *= 0.75
        print("⚠️ Penalización: WR < 50% (-25%)")
    if nivel_honor <= 1:
        pago_final *= 0.50
        print("⚠️ Penalización: Honor 0-1 (-50%)")
    return pago_final

def mostrar_reporte(lista_pedidos):
    limpiar_pantalla()
    print("\n" + "="*45)
    print("📊 HISTORIAL DE ELO-BOOST 📊")
    print("="*45)
    if not lista_pedidos:
        print("No hay pedidos registrados aún.")
    else:
        total_caja = 0
        for i, p in enumerate(lista_pedidos, 1):
            print(f"{i}. [{p['estado']}] {p['cuenta']} | Profit: ${p['ganancia']}")
            if p['estado'] == "Terminado":
                total_caja += p['ganancia']
        print("-" * 45)
        print(f"💰 GANANCIA TOTAL ACUMULADA: ${total_caja}")
    print("=" * 45)
    input("\nPresiona Enter para volver al menú...")

def pedir_numero(mensaje):
    while True:
        try: return int(input(mensaje))
        except ValueError: print("❌ Ingresa solo números.")

def pedir_si_no(mensaje):
    while True:
        res = input(mensaje).lower()
        if res == 's': return True
        if res == 'n': return False

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# --- ZONA PRINCIPAL CON MENÚ ---

pedidos = cargar_datos()

while True:
    
    print("1. Registrar nuevo pedido")
    print("2. Ver historial y total en caja")
    print("3. Buscar pedido específico") # Nueva opción
    print("4. Marcar pedido como Terminado") # Nueva opción
    print("5. Borrar historial (Reset)")
    print("6. Salir")
    
    # --- DENTRO DEL WHILE TRUE ---
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        # ... (Tu código actual para registrar pedido)
        # Asegúrate de que al final del registro diga: pedidos.append(nuevo_ticket)
        # y guardar_datos(pedidos)
        pass 

    elif opcion == "2":
        mostrar_reporte(pedidos)

    elif opcion == "3":
        buscar_pedido(pedidos)  # <--- NUEVA

    elif opcion == "4":
        actualizar_estado(pedidos) # <--- NUEVA
        guardar_datos(pedidos)     # Guardamos el cambio en el archivo .json

    elif opcion == "5":
        if pedir_si_no("¿SEGURO que quieres borrar TODO el historial? (s/n): "):
            pedidos = []
            if os.path.exists("base_datos_pedidos.json"):
                os.remove("base_datos_pedidos.json")
            print("\n🔥 Historial borrado.")
            input("Presiona Enter...")

    elif opcion == "6":
        print("\n¡Nos vemos, Manager! Suerte con los rangos.")
        break