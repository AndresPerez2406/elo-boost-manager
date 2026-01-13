import json
import os

# --- ZONA DE FUNCIONES ---

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
    limpiar_pantalla()
    print("--- PEREZBOOST MANAGER v3.0 ---")
    print("1. Registrar nuevo pedido")
    print("2. Ver historial y total en caja")
    print("3. Borrar historial (Reset)")
    print("4. Salir")
    
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        limpiar_pantalla()
        print("--- NUEVO PEDIDO ---")
        cuenta = input("Nombre de Cuenta: ")
        booster = input("Nombre del Booster: ")
        precio_cliente = pedir_numero("Cobro al Cliente ($): ")
        pago_base = pedir_numero("Pago base al Booster ($): ")
        wr = pedir_numero("Win Rate final (%): ")
        honor = pedir_numero("Nivel de Honor (0-5): ")
        
        pago_real = calcular_pago_booster(pago_base, wr, honor)
        profit = precio_cliente - pago_real
        estado = "Terminado" if pedir_si_no("¿Ya terminó? (s/n): ") else "Pendiente"

        pedidos.append({
            "cuenta": cuenta, "booster": booster, "pago_booster": pago_real,
            "ganancia": profit, "estado": estado
        })
        guardar_datos(pedidos)
        print(f"\n✅ Guardado. Profit: ${profit}")
        input("Presiona Enter...")

    elif opcion == "2":
        mostrar_reporte(pedidos)

    elif opcion == "3":
        if pedir_si_no("¿SEGURO que quieres borrar TODO el historial? (s/n): "):
            pedidos = []
            if os.path.exists("base_datos_pedidos.json"):
                os.remove("base_datos_pedidos.json")
            print("\n🔥 Historial borrado.")
            input("Presiona Enter...")

    elif opcion == "4":
        print("\n¡Nos vemos, Manager! Suerte con los rangos.")
        break
    else:
        print("❌ Opción inválida.")
        input("Presiona Enter...")