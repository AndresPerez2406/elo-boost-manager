import json
import os
import csv
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN Y PRECIOS
# ==========================================
PRECIOS_ELO = {
    "D4": 30, "D3": 30, "D2": 35, "D1": 45,
    "E4": 12, "E3": 12, "E2": 15, "E1": 18,
    "P4": 8, "P3": 8, "P2": 10, "P1": 10
}

# ==========================================
# GESTIÓN DE ARCHIVOS
# ==========================================

def cargar_datos():
    if os.path.exists("base_datos_pedidos.json"):
        try:
            with open("base_datos_pedidos.json", "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except json.JSONDecodeError:
            return {"pedidos": [], "disponibles": []}
    return {"pedidos": [], "disponibles": []}

def guardar_datos(datos_completos):
    with open("base_datos_pedidos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos_completos, archivo, indent=4, ensure_ascii=False)
    print("\n💾 Guardado exitosamente.")

def exportar_a_csv(lista_pedidos):    
    if not lista_pedidos:
        print("⚠️ No hay datos para exportar.")
        return

    nombre_archivo = "reporte_perezboost_v4.csv"
    columnas = [
        "booster", "tipo_cuenta", "user_pass", "estado", 
        "elo_final", "wr", "pago_cliente", "ganancia_empresa", 
        "pago_booster", "bono_aplicado", "fecha_inicio", "fecha_limite"
    ]

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8-sig') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas, extrasaction='ignore')
            escritor.writeheader()
            escritor.writerows(lista_pedidos)
        print(f"\n✅ ¡Excel generado! Archivo: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
    input("\nPresiona Enter para continuar...")

# ==========================================
# INVENTARIO (VERSIÓN SIMPLE)
# ==========================================

def registrar_en_inventario(disponibles):
    print("\n--- 📥 RECIBIR CUENTA DE CLIENTE ---")
    user_pass = input("Pega el User:Pass: ").strip()
    elo = input("Elo de la cuenta (D/E): ").upper()
    
    if elo not in ["D", "E", "P"]: 
        print("⚠️ Elo no reconocido (Usa D para Diamante, E para el resto).")
        elo = "E"

    nueva_cuenta = {"user_pass": user_pass, "elo": elo}
    disponibles.append(nueva_cuenta)
    print(f"✅ Cuenta guardada en bodega.")

def registro_masivo_inventario(disponibles):
    print("\n--- 📥 REGISTRO MASIVO ---")
    print("Pega la lista y escribe 'FIN' al terminar:")
    
    lineas = []
    while True:
        linea = input()
        if linea.upper() == "FIN":
            break
        if ":" in linea:
            lineas.append(linea)
    
    if not lineas:
        print("⚠️ No se detectaron cuentas válidas.")
        return

    print("\n¿Categoría del lote? (D/E): ")
    tipo_lote = input("Selecciona: ").upper().strip()
    
    cuentas_agregadas = 0
    for l in lineas:
        nueva_cuenta = {"user_pass": l.strip(), "elo": tipo_lote}
        disponibles.append(nueva_cuenta)
        cuentas_agregadas += 1
    print(f"✅ Se agregaron {cuentas_agregadas} cuentas al inventario.")

def ver_inventario(disponibles):
    print("\n--- 📦 CUENTAS DISPONIBLES EN BODEGA ---")
    traductor_elo = {"D": "DIAMANTE", "E": "ESMERALDA/PLATINO", "P": "PLATINO"}
    
    if not disponibles:
        print("   (La bodega está vacía)")
    else:
        for i, cuenta in enumerate(disponibles):
            elo_visual = traductor_elo.get(cuenta['elo'], "VARIOS")
            print(f"{i+1}. [{elo_visual}] - {cuenta['user_pass']}")
    input("\nPresiona Enter para continuar...")

# ==========================================
# GESTIÓN DE PEDIDOS
# ==========================================

def asignar_desde_inventario(pedidos, disponibles):
    if not disponibles:
        print("\n⚠️ Bodega vacía. Ve a la Opción 1.")
        return False

    print("\n--- 📝 ASIGNAR CUENTA A BOOSTER ---")
    traductor_elo = {"D": "DIAMANTE", "E": "ESMERALDA/PLATINO"}
    
    for i, c in enumerate(disponibles):
        elo_v = traductor_elo.get(c['elo'], "VARIOS")
        print(f"{i+1}. [{elo_v}] - {c['user_pass']}")

    try:
        sel = int(input("\nNúmero de cuenta (0 para cancelar): "))
        if sel == 0: return False
        
        # Saca la cuenta del inventario
        cuenta_elegida = disponibles.pop(sel - 1) 
        
        # AQUÍ ES MANUAL (NO HAY LISTA DE BOOSTERS)
        booster = input(f"¿A qué booster le das: {cuenta_elegida['user_pass']}?: ").strip()
        tipo = cuenta_elegida['elo'] 

        dias_limite = 15 if tipo == "D" else 10
        f_inicio = datetime.now()
        f_limite = f_inicio + timedelta(days=dias_limite)

        nuevo_pedido = {
            "user_pass": cuenta_elegida['user_pass'],
            "booster": booster,
            "tipo_cuenta": tipo,
            "fecha_inicio": f_inicio.strftime("%d/%m/%Y"),
            "fecha_limite": f_limite.strftime("%d/%m/%Y"),
            "estado": "Pendiente",
            "pago_cliente": 0.0,
            "ganancia_empresa": 0.0,
            "pago_booster": 0.0,
            "wr": 0,
            "bono_aplicado": "NO",
            "elo_final": "Pendiente"
        }
        
        pedidos.append(nuevo_pedido)
        print(f"\n✅ ASIGNADO A {booster.upper()}.")
        print(f"   ⏳ Plazo: {dias_limite} días")
        return True 
    except (ValueError, IndexError):
        print("❌ Selección inválida.")
        return False

def actualizar_estado(lista_pedidos):
    if not lista_pedidos:
        print("⚠️ No hay pedidos activos.")
        return

    print("\n--- ✅ TERMINAR PEDIDO ---")
    indices_pendientes = []
    
    for i, p in enumerate(lista_pedidos):
        if p.get('estado') == "Pendiente":
            indices_pendientes.append(i)
            print(f"{len(indices_pendientes)}. {p['booster']} | {p['user_pass']}")

    if not indices_pendientes:
        print("✅ No hay pedidos pendientes.")
        return

    try:
        seleccion = int(input("\nNúmero del pedido a cerrar (0 cancelar): "))
        if seleccion == 0: return
        
        indice_real = indices_pendientes[seleccion - 1]
        p = lista_pedidos[indice_real] 
    except (ValueError, IndexError):
        print("❌ Selección inválida.")
        return

    print(f"\nCerrando pedido de: {p['booster']}")
    elo_f = input("¿División final lograda? (ej: D2, E1, P4): ").strip().upper()
    
    if elo_f not in PRECIOS_ELO:
        print("❌ División no existe en la tabla de precios.")
        return

    pago_total = PRECIOS_ELO[elo_f]
    mi_ganancia = 10.0 if p.get('tipo_cuenta') == "D" else 5.0
    pago_booster = pago_total - mi_ganancia
    
    try:
        wr_f = float(input("¿Win Rate final? (Solo número): "))
    except ValueError:
        wr_f = 0.0
        
    if wr_f >= 60:
        pago_booster += 1.0
        p['bono_aplicado'] = "SÍ"
        print("🔥 ¡Bono de WR aplicado!")
    else:
        p['bono_aplicado'] = "NO"

    p['elo_final'] = elo_f
    p['wr'] = wr_f
    p['pago_cliente'] = pago_total
    p['ganancia_empresa'] = mi_ganancia
    p['pago_booster'] = pago_booster
    p['estado'] = "Terminado"

    print(f"\n💰 BOOSTER GANA: ${pago_booster}")
    print(f"🏢 TU GANAS:      ${mi_ganancia}")
    input("Presiona Enter para continuar...")

def buscar_pedido(lista_pedidos):
    # BUSQUEDA MANUAL (NO HAY LISTA PRECARGADA)
    nombre = input("\n🔍 Nombre del Booster: ").strip().lower()
    encontrado = False
    print(f"\n--- PENDIENTES DE {nombre.upper()} ---")
    
    for p in lista_pedidos:
        if p['booster'].lower() == nombre and p['estado'] == "Pendiente":
            try:
                limite = datetime.strptime(p.get('fecha_limite', ''), "%d/%m/%Y")
                hoy = datetime.now()
                restantes = (limite - hoy).days
                alerta = f"{restantes} días rest." if restantes >= 0 else "ATRASADO"
            except:
                alerta = "Sin fecha"

            print(f"🔹 {p['user_pass']} | {alerta}")
            encontrado = True
            
    if not encontrado:
        print("✅ Este booster no tiene cuentas pendientes.")
    input("\nPresiona Enter para continuar...")

def mostrar_reporte(lista_pedidos):
    if not lista_pedidos:
        print("\n📭 Historial vacío.")
        input("Enter...")
        return

    total_empresa = 0
    total_boosters = 0
    
    print("\n" + "="*115)
    print(f"{'BOOSTER':<12} | {'ELO/TIPO':<10} | {'ESTADO':<15} | {'CUENTA':<25} | {'EMPRESA':<8} | {'BONO':<5}")
    print("-" * 115)
    
    for p in lista_pedidos:
        estado = p.get('estado', 'Pendiente')
        vista_elo = p.get('elo_final', '---') if estado == "Terminado" else p.get('tipo_cuenta', 'E')
        
        ganancia_e = p.get('ganancia_empresa', 0)
        pago_b = p.get('pago_booster', 0)
        booster = p.get('booster', '---')
        cuenta = p.get('user_pass', '---')
        bono = p.get('bono_aplicado', 'NO')

        print(f"{booster[:12]:<12} | {vista_elo:<10} | {estado:<15} | {cuenta[:25]:<25} | ${ganancia_e:<7.2f} | {bono:<5}")
        
        if estado == "Terminado":
            total_empresa += ganancia_e
            total_boosters += pago_b

    print("-" * 115)
    print(f"📊 NETO EMPRESA:  ${total_empresa:.2f}")
    print(f"💸 PAGO BOOSTERS: ${total_boosters:.2f}")
    print("="*115)
    input("\nPresiona Enter para continuar...")

# ==========================================
# MAIN LOOP (VERSIÓN V4)
# ==========================================

def main():
    datos = cargar_datos()
    pedidos = datos["pedidos"]        
    disponibles = datos["disponibles"] 

    while True:
        print("\n" + "█"*40)
        print("   PEREZBOOST MANAGER v4.0 (LEGACY)")
        print("█"*40)
        print("1. 📥 Recibir cuenta (Inventario)")
        print("2. 📝 Asignar cuenta a Booster")
        print("3. 📊 Ver Reporte y Caja")
        print("4. 🔍 Buscar Cuentas de un Booster")
        print("5. ✅ Terminar Pedido (Cobrar)")
        print("6. 📈 Exportar Excel (.csv)")
        print("7. 📦 Ver Bodega")
        print("8. 🔥 Resetear Todo")
        print("9. 🚪 Salir")
        
        opcion = input("\n>>> Selecciona: ")

        if opcion == "1":
            print("\n1. Individual\n2. Masivo (Lista)")
            sub = input("Opción: ")
            if sub == "1": registrar_en_inventario(disponibles)
            elif sub == "2": registro_masivo_inventario(disponibles)
            guardar_datos(datos)

        elif opcion == "2":
            if asignar_desde_inventario(pedidos, disponibles):
                guardar_datos(datos)

        elif opcion == "3":
            mostrar_reporte(pedidos)

        elif opcion == "4":
            buscar_pedido(pedidos)

        elif opcion == "5":
            actualizar_estado(pedidos)
            guardar_datos(datos)

        elif opcion == "6":
            exportar_a_csv(pedidos)

        elif opcion == "7":
            ver_inventario(disponibles)

        elif opcion == "8":
            if input("¿SEGURO? (s/n): ") == 's':
                datos["pedidos"] = []
                datos["disponibles"] = []
                guardar_datos(datos)
                print("🔥 Sistema reiniciado.")

        elif opcion == "9":
            print("\n¡Nos vemos!")
            break

if __name__ == "__main__":
    main()