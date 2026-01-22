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
    """Carga la base de datos y asegura que existan todas las listas necesarias."""
    estructura_base = {"pedidos": [], "disponibles": [], "boosters": []}
    
    if os.path.exists("base_datos_pedidos.json"):
        try:
            with open("base_datos_pedidos.json", "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                # Inyección de dependencias para versiones viejas
                if "boosters" not in datos: datos["boosters"] = []
                if "disponibles" not in datos: datos["disponibles"] = []
                return datos
        except json.JSONDecodeError:
            print("⚠️ Archivo dañado. Se creará uno nuevo.")
            return estructura_base
    return estructura_base

def guardar_datos(datos_completos):
    with open("base_datos_pedidos.json", "w", encoding="utf-8") as archivo:
        json.dump(datos_completos, archivo, indent=4, ensure_ascii=False)
    print("\n💾 Guardado exitosamente.")

def exportar_a_csv(lista_pedidos):    
    if not lista_pedidos:
        print("⚠️ No hay datos para exportar.")
        return

    nombre_archivo = "reporte_perezboost_final.csv"
    columnas = [
        "booster", "tipo_cuenta", "user_pass", "estado", 
        "elo_final", "wr", "pago_cliente", "ganancia_empresa", 
        "pago_booster", "bono_aplicado", "fecha_inicio", "fecha_limite"
    ]

    # Traducción para Excel (D -> Diamante)
    datos_para_excel = []
    for p in lista_pedidos:
        fila = p.copy()
        if fila.get('tipo_cuenta') == 'D':
            fila['tipo_cuenta'] = 'Diamante'
        else:
            fila['tipo_cuenta'] = 'Esmeralda/Platino'
        datos_para_excel.append(fila)

    try:
        with open(nombre_archivo, mode='w', newline='', encoding='utf-8-sig') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas, extrasaction='ignore')
            escritor.writeheader()
            escritor.writerows(datos_para_excel)
        print(f"\n✅ ¡Excel generado! Archivo: {nombre_archivo}")
    except Exception as e:
        print(f"❌ Error al exportar: {e}")
    input("\nPresiona Enter para continuar...")

# ==========================================
# GESTIÓN DE EQUIPO (BOOSTERS)
# ==========================================

def administrar_boosters(boosters):
    while True:
        print("\n--- 👥 GESTIÓN DE EQUIPO (BOOSTERS) ---")
        print("1. Ver lista de Boosters")
        print("2. Contratar (Agregar Nuevo)")
        print("3. Despedir (Eliminar)")
        print("4. Volver al Menú Principal")
        
        op = input("Selecciona: ")
        
        if op == "1":
            if not boosters:
                print("   (No hay boosters registrados)")
            else:
                print("\n   NOMINA ACTUAL:")
                for i, b in enumerate(boosters):
                    print(f"   {i+1}. {b}")
        
        elif op == "2":
            nombre = input("Nombre del nuevo Booster: ").strip().title()
            if not nombre: 
                print("❌ Error: El nombre no puede estar vacío.")
            elif nombre in boosters:
                print(f"❌ El booster '{nombre}' ya existe.")
            else:
                boosters.append(nombre)
                print(f"✅ {nombre} agregado al equipo.")
        
        elif op == "3":
            if not boosters:
                print("⚠️ No hay nadie a quien despedir.")
            else:
                print("\n   SELECCIONA PARA ELIMINAR:")
                for i, b in enumerate(boosters):
                    print(f"   {i+1}. {b}")
                try:
                    elim = int(input("Número: "))
                    if 1 <= elim <= len(boosters):
                        borrado = boosters.pop(elim - 1)
                        print(f"🗑️ {borrado} eliminado de la lista.")
                    else:
                        print("❌ Número fuera de rango.")
                except ValueError:
                    print("❌ Debes escribir un número.")
        
        elif op == "4":
            return 

# ==========================================
# INVENTARIO (CON PROTECCIÓN DE DUPLICADOS)
# ==========================================

def registrar_en_inventario(disponibles, pedidos):
    print("\n--- 📥 RECIBIR CUENTA DE CLIENTE ---")
    raw_input = input("Pega el User:Pass: ").strip()
    
    # Limpieza Universal
    limpia = raw_input.replace("-----", " : ").replace("----", " : ").replace("---", " : ")
    limpia = limpia.replace("|", " : ")
    
    # Validación Duplicados
    for c in disponibles:
        if c['user_pass'] == limpia:
            print(f"❌ ERROR: La cuenta '{limpia}' YA está en la bodega.")
            return False 

    for p in pedidos:
        if p['user_pass'] == limpia:
            print(f"❌ ERROR: Esa cuenta YA existe en el sistema.")
            return False 

    elo = input("Elo de la cuenta (D/E): ").upper()
    if elo not in ["D", "E", "P"]: 
        print("⚠️ Elo no reconocido (Usa D para Diamante, E para el resto).")
        elo = "E" 

    disponibles.append({"user_pass": limpia, "elo": elo})
    print(f"✅ Cuenta guardada: {limpia}")
    return True 

def registro_masivo_inventario(disponibles, pedidos):
    print("\n--- 📥 REGISTRO MASIVO ---")
    print("Pega la lista y escribe 'FIN' al terminar:")
    
    lineas = []
    while True:
        linea = input()
        if linea.upper() == "FIN":
            break
        if ":" in linea or "-" in linea:
            lineas.append(linea)
    
    if not lineas:
        return False

    print("\n¿Categoría del lote? (D/E): ")
    tipo_lote = input("Selecciona: ").upper().strip()
    if tipo_lote not in ["D", "E", "P"]:
        print("❌ Tipo no válido.")
        return False

    agregadas = 0
    rechazadas = 0

    for l in lineas:
        limpia = l.strip().replace("-----", " : ").replace("----", " : ").replace("---", " : ")
        limpia = limpia.replace("|", " : ")

        duplicada = False
        for c in disponibles:
            if c['user_pass'] == limpia: duplicada = True
        for p in pedidos:
            if p['user_pass'] == limpia: duplicada = True
            
        if duplicada:
            print(f"   ❌ Saltada (Duplicada): {limpia}")
            rechazadas += 1
        else:
            disponibles.append({"user_pass": limpia, "elo": tipo_lote})
            agregadas += 1
            
    print(f"\n✅ RESUMEN: {agregadas} Agregadas | {rechazadas} Rechazadas.")
    return agregadas > 0

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
# GESTIÓN DE PEDIDOS (ASIGNAR / CERRAR)
# ==========================================

def asignar_desde_inventario(pedidos, disponibles, boosters):
    if not disponibles:
        print("\n⚠️ Bodega vacía. Ve a la Opción 1.")
        return False
    
    if not boosters:
        print("\n⚠️ NO TIENES BOOSTERS REGISTRADOS.")
        print("   Ve a la Opción 8 primero.")
        input("Enter...")
        return False

    print("\n--- 📦 SELECCIONA CUENTA ---")
    traductor_elo = {"D": "DIAMANTE", "E": "ESMERALDA/PLATINO"}
    for i, c in enumerate(disponibles):
        elo_v = traductor_elo.get(c['elo'], "VARIOS")
        print(f"{i+1}. [{elo_v}] - {c['user_pass']}")

    try:
        sel_cta = int(input("\nNúmero de cuenta (0 cancelar): "))
        if sel_cta == 0: return False
        
        print("\n--- 👤 SELECCIONA EL BOOSTER ---")
        for i, b in enumerate(boosters):
            print(f"{i+1}. {b}")
            
        sel_b = int(input("Número del Booster: "))
        if sel_b < 1 or sel_b > len(boosters):
            print("❌ Número de booster inválido.")
            return False

        nombre_booster = boosters[sel_b - 1]
        
        cuenta_elegida = disponibles.pop(sel_cta - 1) 
        tipo = cuenta_elegida['elo'] 

        dias_limite = 15 if tipo == "D" else 10
        f_inicio = datetime.now()
        f_limite = f_inicio + timedelta(days=dias_limite)

        nuevo_pedido = {
            "user_pass": cuenta_elegida['user_pass'],
            "booster": nombre_booster,
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
        print(f"\n✅ ASIGNADO A {nombre_booster.upper()}.")
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
            tipo_raw = p.get('tipo_cuenta', 'E')
            tipo_texto = "DIAMANTE" if tipo_raw == "D" else "ESMERALDA/PLATINO"
            print(f"{len(indices_pendientes)}. {p['booster']} | {p['user_pass']} [ Meta: {tipo_texto} ]")

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

def buscar_pedido(lista_pedidos, boosters):
    if not boosters:
        print("\n⚠️ No hay boosters registrados.")
        return

    print("\n--- 🔍 BUSCAR CUENTAS POR BOOSTER ---")
    for i, b in enumerate(boosters):
        print(f"{i+1}. {b}")
    
    try:
        sel = int(input("\nSelecciona el número del Booster: "))
        if sel < 1 or sel > len(boosters):
            print("❌ Número inválido.")
            return
        nombre = boosters[sel - 1]
    except ValueError:
        print("❌ Debes escribir un número.")
        return

    encontrado = False
    print(f"\n--- 📋 PENDIENTES DE: {nombre.upper()} ---")
    
    for p in lista_pedidos:
        if p['booster'] == nombre and p['estado'] == "Pendiente":
            try:
                limite = datetime.strptime(p.get('fecha_limite', ''), "%d/%m/%Y")
                hoy = datetime.now()
                restantes = (limite - hoy).days
                if restantes < 0:
                    alerta = f"⛔ TARDE POR {-restantes} DÍAS"
                else:
                    alerta = f"⏳ Quedan {restantes} días"
            except:
                alerta = "Sin fecha"

            print(f"🔹 {p['user_pass']} | {alerta}")
            encontrado = True
            
    if not encontrado:
        print(f"✅ {nombre} no tiene cuentas pendientes.")
    input("\nPresiona Enter para continuar...")

def mostrar_reporte(lista_pedidos):
    if not lista_pedidos:
        print("\n📭 Historial vacío.")
        input("Enter...")
        return

    total_empresa = 0
    total_boosters = 0
    
    print("\n" + "="*115)
    print(f"{'BOOSTER':<12} | {'ELO/TIPO':<15} | {'ESTADO/DIAS':<15} | {'CUENTA':<25} | {'EMPRESA':<8} | {'BONO':<5}")
    print("-" * 115)
    
    for p in lista_pedidos:
        estado = p.get('estado', 'Pendiente')
        
        if estado == "Terminado":
            columna_estado = "TERMINADO"
            vista_elo = p.get('elo_final', '---')
        else:
            tipo_raw = p.get('tipo_cuenta', 'E')
            vista_elo = "Diamante" if tipo_raw == "D" else "Esm/Plat"

            try:
                limite = datetime.strptime(p.get('fecha_limite', ''), "%d/%m/%Y")
                hoy = datetime.now()
                dias = (limite - hoy).days
                if dias < 0:
                    columna_estado = f"⛔ {-dias}d TARDE"
                else:
                    columna_estado = f"⏳ {dias}d rest."
            except:
                columna_estado = "Pendiente"

        ganancia_e = p.get('ganancia_empresa', 0)
        pago_b = p.get('pago_booster', 0)
        booster = p.get('booster', '---')
        cuenta = p.get('user_pass', '---')
        bono = p.get('bono_aplicado', 'NO')

        print(f"{booster[:12]:<12} | {vista_elo:<15} | {columna_estado:<15} | {cuenta[:25]:<25} | ${ganancia_e:<7.2f} | {bono:<5}")
        
        if estado == "Terminado":
            total_empresa += ganancia_e
            total_boosters += pago_b

    print("-" * 115)
    print(f"📊 NETO EMPRESA:  ${total_empresa:.2f}")
    print(f"💸 PAGO BOOSTERS: ${total_boosters:.2f}")
    print("="*115)
    input("\nPresiona Enter para continuar...")

# ==========================================
# BUCLE PRINCIPAL (MAIN)
# ==========================================

def main():
    datos = cargar_datos()
    pedidos = datos["pedidos"]        
    disponibles = datos["disponibles"] 
    boosters = datos["boosters"]

    while True:
        # os.system('cls' if os.name == 'nt' else 'clear') 
        print("\n" + "█"*40)
        print("   PEREZBOOST MANAGER v4.3 (MASTER)")
        print("█"*40)
        print("1. 📥 Recibir cuenta (Inventario)")
        print("2. 📝 Asignar cuenta a Booster")
        print("3. 📊 Ver Reporte y Caja")
        print("4. 🔍 Buscar Cuentas de un Booster")
        print("5. ✅ Terminar Pedido (Cobrar)")
        print("6. 📈 Exportar Excel (.csv)")
        print("7. 📦 Ver Bodega")
        print("8. 👥 Gestión de Equipo (Boosters)")
        print("9. 🔥 Resetear Todo")
        print("10. 🚪 Salir")
        
        opcion = input("\n>>> Selecciona: ")

        if opcion == "1":
            print("\n1. Individual\n2. Masivo")
            sub = input("Opción: ")
            hubo_cambios = False
            if sub == "1": hubo_cambios = registrar_en_inventario(disponibles, pedidos)
            elif sub == "2": hubo_cambios = registro_masivo_inventario(disponibles, pedidos)
            
            if hubo_cambios: guardar_datos(datos)
            else: print("(Sin cambios en base de datos)")

        elif opcion == "2":
            if asignar_desde_inventario(pedidos, disponibles, boosters):
                guardar_datos(datos)

        elif opcion == "3":
            mostrar_reporte(pedidos)

        elif opcion == "4":
            buscar_pedido(pedidos, boosters)

        elif opcion == "5":
            actualizar_estado(pedidos)
            guardar_datos(datos)

        elif opcion == "6":
            exportar_a_csv(pedidos)

        elif opcion == "7":
            ver_inventario(disponibles)

        elif opcion == "8":
            administrar_boosters(boosters)
            guardar_datos(datos)

        elif opcion == "9":
            if input("¿SEGURO? (s/n): ") == 's':
                datos["pedidos"] = []
                datos["disponibles"] = []
                # Boosters se conservan
                guardar_datos(datos)
                print("🔥 Historial borrado.")

        elif opcion == "10":
            print("\n¡A darle duro, Manager! Nos vemos.")
            break

if __name__ == "__main__":
    main()