import os
from core.database import (
    obtener_boosters_db,              
    obtener_cuentas_disponibles_por_elo, 
    crear_pedido, 
    obtener_pedidos_activos, 
    finalizar_pedido_db, 
    obtener_historial,
    obtener_boosters_activos_db,
    obtener_pedidos_por_booster_id,
    obtener_pedido_por_id,
    actualizar_fecha_limite_db,
    registrar_abandono_db
)

from core.logic import (
    normalizar_elo, 
    calcular_fecha_limite_sugerida,
    calcular_tiempo_transcurrido,
    calcular_pago_real,
    extender_fecha
)

def menu_pedidos():
    while True:
        print("\n" + "⚔️  GESTIÓN DE PEDIDOS (V6)".center(40, "="))
        print("1. 📜 Ver Activos")
        print("2. ⚡ Asignar Nuevo Pedido")
        print("3. 🔍 Buscar por Booster")
        print("4. ⏳ Extender Plazo")
        print("5. ✅ Finalizar (Cierre Express)")
        print("6. 💰 Historial de Finalizados")
        print("7. 🚫 Reportar Abandono")
        print("8. 🔙 Volver")
        
        op = input("\n>>> Seleccione una opción: ").strip()
        
        if op == "1": listar_activos()
        elif op == "2": nuevo_pedido()
        elif op == "3": buscar_por_booster()
        elif op == "4": extender_plazo()
        elif op == "5": terminar_trabajo()
        elif op == "6": ver_historial()
        elif op == "7": reportar_abandono()
        elif op == "8": break
        else: print("❌ Opción no válida.")

# --------------------------------------------------------------------------
# LISTADO
# --------------------------------------------------------------------------

def listar_activos():
    """
    Muestra la tabla de pedidos con 6 columnas:
    ID | BOOSTER | CUENTA | INICIO | FIN | TIEMPO ACTIVA
    """
    print("\n" + "--- 📜 LISTADO DE PEDIDOS ACTIVOS ---".center(95))
    pedidos = obtener_pedidos_activos()
    
    if not pedidos:
        print("   (No hay pedidos activos en este momento)".center(95))
        return False

    header = f"{'ID':<4} | {'BOOSTER':<12} | {'CUENTA':<18} | {'INICIO':<16} | {'FIN':<16} | {'TIEMPO ACTIVA'}"
    print(header)
    print("-" * 95)
    
    for pid, b_nom, elo, user_pass, f_ini, f_lim in pedidos:
        
        # Acortamos el usuario para no romper la fila
        cuenta_display = (user_pass[:16] + '..') if len(user_pass) > 16 else user_pass
        
        # Calculamos el tiempo que lleva activa la cuenta
        tiempo_activa = calcular_tiempo_transcurrido(f_ini)
        
        # Imprimimos la fila respetando los anchos del header
        print(f"{pid:<4} | {b_nom:<12} | {cuenta_display:<18} | {f_ini:<16} | {f_lim:<16} | {tiempo_activa}")
    
    print("-" * 95)
    return True

# --------------------------------------------------------------------------
# ACCIONES PRINCIPALES
# --------------------------------------------------------------------------

def reportar_abandono():
    print("\n--- 🚫 REPORTE DE ABANDONO ---")
    
    # 1. FRENO DE MANO: Si listar_activos devuelve False, nos vamos.
    hay_pedidos = listar_activos()
    if not hay_pedidos:
        return 

    try:
        id_ped = int(input("\nID del pedido abandonado: "))
        
        # Validamos visualmente que el usuario no meta un ID cualquiera
        # (Aunque la DB lo validaría igual, esto ahorra tiempo)
        
        elo = input("Elo actual de la cuenta: ").strip().upper()
        wr = input("WR actual (%): ").strip()
        
        print(f"⚠️  Estás a punto de cancelar el pedido #{id_ped}.")
        if input("¿Confirmar abandono? (S/N): ").upper() == "S":
            # Llamamos a tu DB blindada
            if registrar_abandono_db(id_ped, elo, wr):
                # El mensaje de éxito ya lo imprime la DB
                pass
            else:
                print("❌ No se pudo registrar el abandono.")
    except ValueError:
        print("❌ Error: ID debe ser numérico.")

def terminar_trabajo():
    print("\n--- ✅ FINALIZAR PEDIDO ---")
    
    # 1. FRENO DE MANO
    if not listar_activos():
        return

    try:
        id_ped = int(input("\nIngrese ID del Pedido a finalizar: "))
    except ValueError:
        print("❌ ID inválido.")
        return

    div_final = input("División Final: ").strip().upper()
    try:
        wr_final = float(input("Winrate Final (%): "))
    except ValueError:
        print("❌ Winrate debe ser un número.")
        return

    # Ajustes
    ajuste = 0.0
    motivo = ""
    if input("¿Hubo ajuste/bono? (S/N): ").upper() == "S":
        try:
            ajuste = float(input("Monto ($): "))
            motivo = input("Motivo: ")
        except: pass

    # Cálculo
    cobro_cli, pago_boo, ganancia = calcular_pago_real(div_final, wr_final, ajuste)

    if cobro_cli == 0:
        print("⚠️ Error: División desconocida o sin precio.")
        return

    print("-" * 30)
    print(f"💰 Cliente:  ${cobro_cli}")
    print(f"🤝 Booster:  ${pago_boo}")
    print(f"🏦 Empresa:  ${ganancia}")
    print("-" * 30)
    
    if input("¿Guardar y Cerrar? (S/N): ").upper() == "S":
        finalizar_pedido_db(id_ped, div_final, wr_final, cobro_cli, pago_boo, ganancia, ajuste, motivo)
        print("✅ Pedido finalizado correctamente.")

# --------------------------------------------------------------------------
# OTRAS FUNCIONES (NUEVO, BUSCAR, EXTENDER...)
# --------------------------------------------------------------------------

def nuevo_pedido():
    print("\n--- ⚡ NUEVO PEDIDO ---")
    boosters = obtener_boosters_db()
    if not boosters:
        print("❌ No hay boosters registrados.")
        return

    print("Staff disponible:")
    for b in boosters: print(f"{b[0]} {b[1]}")
    
    try:
        id_b = int(input("ID Booster: "))
        nombre_b = next((b[1] for b in boosters if b[0] == id_b), None)
        if not nombre_b: 
            print("❌ ID incorrecto.")
            return
    except: return

    busqueda = input("Elo objetivo (ej: D, E): ").strip()
    elo_norm = normalizar_elo(busqueda)
    cuentas = obtener_cuentas_disponibles_por_elo(elo_norm)
    
    if not cuentas:
        print(f"❌ No hay cuentas {elo_norm}.")
        return

    print(f"Cuentas {elo_norm}:")
    for c in cuentas: print(f" {c[0]} | {c[1]} | {c[2]}")
    
    try:
        id_c = int(input("ID Cuenta: "))
        cta = next((c for c in cuentas if c[0] == id_c), None)
        if not cta: return
    except: return

    dias = 10
    f_lim = calcular_fecha_limite_sugerida(dias)
    if crear_pedido(id_b, nombre_b, id_c, cta[1], elo_norm, f_lim):
        print("✅ Asignado.")

def buscar_por_booster():
    print("\n--- 🔍 BUSCAR POR BOOSTER ---")
    boosters = obtener_boosters_activos_db()
    if not boosters:
        print("⚠️ No hay boosters trabajando ahora.")
        return
    
    for b in boosters: print(f"{b[0]} : {b[1]}")
    try:
        idx = int(input("ID Booster: "))
        peds = obtener_pedidos_por_booster_id(idx)
        if peds:
            print(f"{'':<4} | {'CUENTA':<20} | {'DEADLINE'}")
            for p in peds: print(f" {p[0]:<4} | {p[3]:<20} | {p[5]}")
        else:
            print("❌ Sin trabajos activos.")
    except: pass

def extender_plazo():
    print("\n--- ⏳ EXTENDER ---")
    if not listar_activos(): return
    try:
        pid = int(input("ID Pedido: "))
        datos = obtener_pedido_por_id(pid)
        if datos:
            print(f"Vence: {datos[1]}")
            dias = int(input("Días extra: "))
            nueva = extender_fecha(datos[1], dias)
            actualizar_fecha_limite_db(pid, nueva)
            print(f"✅ Nueva fecha: {nueva}")
    except: pass

def ver_historial():
    print("\n--- 💰 HISTORIAL ---")
    data = obtener_historial()
    if not data:
        print(" (Vacío)")
        return
    print(f"{'ID':<4}| {'BOOSTER':<10} | {'GANANCIA':<9} | {'FIN'}")
    total = 0
    for row in data:
        total += row[5]
        print(f"{row[0]:<4}| {row[1]:<10} | ${row[5]:<8} | {row[8]}")
    print("-" * 40)
    print(f"TOTAL GANADO: ${total:.2f}")