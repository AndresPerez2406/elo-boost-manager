import json
import os
import csv


# Tabla de precios: Lo que paga el cliente/proveedor

PRECIOS_ELO = {
    "D4": 30, "D3": 30, "D2": 35, "D1": 45,
    "E4": 12, "E3": 12, "E2": 15, "E1": 18,
    "P4": 8, "P3": 8, "P2": 10, "P1": 10
}

# --- ZONA DE FUNCIONES ---

def cargar_datos():
    if os.path.exists("base_datos_pedidos.json"):
        with open("base_datos_pedidos.json", "r") as archivo:
            return json.load(archivo)
    return []

def guardar_datos(lista_pedidos):    
    with open("base_datos_pedidos.json", "w") as archivo:
        json.dump(lista_pedidos, archivo, indent=4)
    print("\n✅ Base de datos actualizada.")

def exportar_a_csv(lista_pedidos):    
    if not lista_pedidos:
        print("⚠️ No hay datos para exportar.")
        return

    nombre_archivo = "reporte_boost_ventas.csv"
    columnas = [
        "user_pass", "booster", "elo_final", "wr",
        "pago_cliente", "ganancia_empresa", "pago_booster", "bono_aplicado", "estado"
    ]

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()  # Escribe los títulos de las columnas
            escritor.writerows(lista_pedidos) # Escribe todos los pedidos de golpe
        
        print(f"\n✅ ¡Éxito! Reporte creado como: {nombre_archivo}")
        print("💡 Ya puedes abrirlo con Excel o Google Sheets.")
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
    
    input("\nPresiona Enter para continuar...")

def registrar_pedido():
    print("\n--- 📝 Registro de Nuevo Pedido ---")
    user_pass = input("Pega el User:Pass: ").strip()
    booster = input("Nombre del Booster: ").strip()
    
    # Solo dos opciones: D o E
    tipo = input("Tipo de cuenta (D: Diamante / E: Esmeralda-Platino): ").strip().upper()

    nuevo_pedido = {
        "user_pass": user_pass,
        "booster": booster,
        "tipo_cuenta": tipo, # Guardamos 'D' o 'E'
        "elo_final": "Pendiente",
        "wr": 0,
        "pago_cliente": 0.0,
        "ganancia_empresa": 0.0,
        "pago_booster": 0.0,
        "estado": "Pendiente"
    }
    return nuevo_pedido

def actualizar_estado(lista_pedidos):
    if not lista_pedidos:
        print("⚠️ No hay pedidos registrados.")
        return

    # 1. Mostrar lista de pendientes
    print("\n--- 📋 PEDIDOS PENDIENTES ACTUALMENTE ---")
    pendientes = [p for p in lista_pedidos if p['estado'] == "Pendiente"]
    if not pendientes:
        print("✅ No hay nada pendiente por cerrar.")
        return
    
    for i, p in enumerate(pendientes, 1):
        # Mostramos el tipo registrado (D o E) para que sepas qué esperar
        tipo_vista = "Diamante" if p.get('tipo_cuenta') == "D" else "Esm/Plat"
        print(f"{i}. Booster: {p['booster']} | Tipo: {tipo_vista} | Cuenta: {p['user_pass']}")

    # 2. Selección del booster
    seleccion = input("\n📝 Escribe el nombre del BOOSTER del pedido a cerrar (o 'cancelar'): ").strip().lower()
    if seleccion == "cancelar": return

    encontrado = False
    for p in lista_pedidos:
        if p['booster'].lower() == seleccion and p['estado'] == "Pendiente":
            print(f"\n✨ Cerrando pedido de {p['booster']}...")
            
            # 3. Pedir Elo Final usando códigos cortos (D2, E1, P4)
            print("Divisiones: D4-D1 | E4-E1 | P4-P1")
            elo_f = input("¿En qué división terminó? (ej: D2): ").strip().upper()
            
            if elo_f not in PRECIOS_ELO:
                print("❌ Código de división no válido. Revisa la tabla de precios.")
                return

            # 4. Cálculo dinámico de ganancia
            pago_total = PRECIOS_ELO[elo_f]
            
            # Si el tipo registrado fue 'D', ganas 10. Si fue 'E', ganas 5.
            mi_ganancia = 10.0 if p.get('tipo_cuenta') == "D" else 5.0

def buscar_pedido(lista_pedidos):
    nombre = input("\n🔍 Nombre del Booster para ver sus cuentas PENDIENTES: ").strip().lower()
    encontrado = False
    print(f"\n--- 📋 CUENTAS PENDIENTES DE: {nombre.upper()} ---")
    
    for p in lista_pedidos:
        # Filtramos por nombre de booster Y que el estado sea Pendiente
        if p['booster'].lower() == nombre and p['estado'] == "Pendiente":
            print(f"🔹 User/Pass: {p['user_pass']}")
            encontrado = True
            
    if not encontrado:
        print("✅ No hay cuentas pendientes para este booster.")
    input("\nPresiona Enter para continuar...")

def mostrar_reporte(lista_pedidos):
    if not lista_pedidos:
        print("\n📭 El historial está vacío.")
        input("\nPresiona Enter para continuar...")
        return

    total_empresa = 0
    total_boosters = 0
    total_bruto_real = 0
    
    # Traductor para la columna ELO cuando el pedido está pendiente
    nombres_completos = {"D": "Diamante", "E": "Esm/Plat"}

    print("\n" + "="*110)
    print(f"{'BOOSTER':<15} | {'ELO/TIPO':<15} | {'CUENTA':<30} | {'ESTADO':<12} | {'EMPRESA':<8} | {'BONO':<5}")
    print("-" * 110)
    
    for p in lista_pedidos:
        # 1. Definir qué mostrar en la columna ELO
        estado = p.get('estado', 'Pendiente')
        if estado == "Terminado":
            vista_elo = p.get('elo_final', '---')
        else:
            letra_tipo = p.get('tipo_cuenta', 'E')
            vista_elo = nombres_completos.get(letra_tipo, "Esm/Plat")

        # 2. Obtener valores financieros
        ganancia_e = p.get('ganancia_empresa', 0)
        pago_b = p.get('pago_booster', 0)
        booster = p.get('booster', '---')
        cuenta = p.get('user_pass', '---')
        bono = p.get('bono_aplicado', 'NO')

        # 3. Imprimir fila de la tabla
        print(f"{booster[:14]:<15} | {vista_elo:<15} | {cuenta[:29]:<30} | {estado:<12} | ${ganancia_e:<7.2f} | {bono:<5}")
        
        # 4. Sumar totales si el pedido está cobrado (Terminado)
        if estado == "Terminado":
            total_empresa += ganancia_e
            total_boosters += pago_b
            # El bruto real es la suma de las dos partes (ya incluye el bono si existe)
            total_bruto_real += (ganancia_e + pago_b)

    # 5. Resumen final de caja
    print("-" * 110)
    print(f"📊 RESUMEN CONTABLE:")
    print(f"🏢 MI GANANCIA NETA:         ${total_empresa:.2f}")
    print(f"💸 TOTAL PAGADO BOOSTERS:    ${total_boosters:.2f}")
    print(f"💰 TOTAL GENERADO:           ${total_bruto_real:.2f}")
    print("="*110)
    input("\nPresiona Enter para continuar...")
    
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
    print("6. Exportar reporte a Excel (.csv)") # NUEVA
    print("7. Salir")
    
    # --- DENTRO DEL WHILE TRUE ---
    opcion = input("\nSelecciona una opción: ")

    if opcion == "1":
        nuevo = registrar_pedido()
        pedidos.append(nuevo) # Lo mete a la lista que vive en memoria
        guardar_datos(pedidos) # Lo escribe en el archivo JSON
        print("\n✅ Pedido registrado con éxito.")
    elif opcion == "2":
        mostrar_reporte(pedidos)

    elif opcion == "3":
        buscar_pedido(pedidos)  # <--- NUEVA

    elif opcion == "4":
        actualizar_estado(pedidos) # <--- NUEVA
        guardar_datos(pedidos)     # Guardamos el cambio en el archivo .json

    elif opcion == "5":
        confirmar = input("¿SEGURO que quieres borrar TODO el historial? (s/n): ").lower()
        if confirmar == 's':
            pedidos = []
            if os.path.exists("base_datos_pedidos.json"):
                os.remove("base_datos_pedidos.json")
            print("\n🔥 Historial borrado.")
            input("Presiona Enter...")

    elif opcion == "6":
        exportar_a_csv(pedidos)
    elif opcion == "7":
        print("\n¡Nos vemos, Manager! Suerte con los rangos.")
        break