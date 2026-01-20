import os
from core.database import obtener_pedidos_activos
from core.database import obtener_historial

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
    extender_fecha,
    calcular_duracion_servicio
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
    Muestra la tabla de pedidos con ID Visual (#) consecutivo.
    Mapea internamente el ID real (pid) pero muestra 1, 2, 3...
    """
    print("\n" + "--- 📜 LISTADO DE PEDIDOS ACTIVOS ---".center(95))
    pedidos = obtener_pedidos_activos()
    
    if not pedidos:
        print("   (No hay pedidos activos en este momento)".center(95))
        return False

    # Cambiamos 'ID' por '#' para indicar que es el número de fila
    header = f"{'#':<4} | {'BOOSTER':<12} | {'CUENTA':<18} | {'INICIO':<16} | {'FIN':<16} | {'TIEMPO'}"
    print(header)
    print("-" * 95)
    
    # Usamos enumerate(pedidos, start=1) para generar el ID Visual
    for i, datos in enumerate(pedidos, start=1):
        # Desempaquetamos los datos reales
        pid, b_nom, elo, user_pass, f_ini, f_lim = datos
        
        # Formateo de cuenta
        cuenta_display = (user_pass[:16] + '..') if len(user_pass) > 16 else user_pass
        
        # Cálculo de tiempo
        tiempo_activa = calcular_tiempo_transcurrido(f_ini)
        
        # Imprimimos usando 'i' como el ID Visual
        print(f"{i:<4} | {b_nom:<12} | {cuenta_display:<18} | {f_ini:<16} | {f_lim:<16} | {tiempo_activa}")
    
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
    print("\n" + "--- 🔍 BUSCAR POR BOOSTER ---".center(50))
    boosters = obtener_boosters_activos_db()
    
    if not boosters:
        print("⚠️ No hay boosters trabajando ahora.")
        return
    
    # Listamos con índice visual para elegir
    for i, b in enumerate(boosters, start=1):
        print(f"{i}: {b[1]}") # b[1] es el nombre
    
    try:
        opcion = int(input("\nSeleccione el # del Booster: "))
        # Obtenemos el ID REAL usando el índice (opcion - 1)
        idx_real = boosters[opcion - 1][0]
        nombre_b = boosters[opcion - 1][1]
        
        peds = obtener_pedidos_por_booster_id(idx_real)
        if peds:
            print(f"\nTrabajos de {nombre_b}:")
            print(f"{'#':<4} | {'CUENTA':<20} | {'DEADLINE'}")
            for j, p in enumerate(peds, start=1):
                print(f" {j:<4} | {p[3]:<20} | {p[5]}")
        else:
            print("❌ Sin trabajos activos.")
    except (ValueError, IndexError):
        print("⚠️ Selección inválida.")

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
    print("\n" + "--- 💰 REPORTE FINANCIERO Y RENDIMIENTO ---".center(115))
    data = obtener_historial()
    
    if not data:
        print(" (El historial está vacío)".center(115))
        return

    # Header con todas las columnas solicitadas
    header = f"{'#':<3} | {'BOOSTER':<12} | {'GAN. B':<9} | {'MI GAN':<9} | {'CLIENTE':<9} | {'INICIO':<12} | {'FIN':<12} | {'DURACIÓN'}"
    print(header)
    print("-" * 115)

    # Acumuladores para los totales
    total_booster = 0
    total_mio = 0
    total_cliente = 0

    for i, row in enumerate(data, start=1):
        # Mapeo según tu SELECT en database.py:
        # row[1]:booster, row[4]:pago_b, row[5]:gan_empresa, row[6]:pago_cliente, row[7]:f_ini, row[8]:f_fin
        booster = row[1]
        gan_b   = row[4] if row[4] else 0
        gan_m   = row[5] if row[5] else 0
        pag_c   = row[6] if row[6] else 0
        f_ini   = row[7]
        f_fin   = row[8]
        
        # Calculamos cuánto demoró (puedes reusar calcular_tiempo_transcurrido o una similar)
        duracion = calcular_duracion_servicio(f_ini, f_fin) 

        # Sumatorias
        total_booster += gan_b
        total_mio     += gan_m
        total_cliente += pag_c

        print(f"{i:<3} | {booster:<12} | ${gan_b:<8.2f} | ${gan_m:<8.2f} | ${pag_c:<8.2f} | {f_ini:<12} | {f_fin:<12} | {duracion}")

    print("-" * 115)
    # EL TOTAL DETALLADO QUE PEDISTE:
    print(f"📊 RESUMEN CONTABLE:")
    print(f"   💰 TOTAL PAGADO A BOOSTERS: ${total_booster:.2f}")
    print(f"   💎 MI GANANCIA NETA TOTAL:  ${total_mio:.2f}")
    print(f"   🏢 TOTAL GENERADO EMPRESA:  ${total_cliente:.2f}")
    print("-" * 115)
    
def obtener_pedidos_visual():
    """Procesa los pedidos activos para la GUI con ID Visual y Tiempo"""
    datos_reales = obtener_pedidos_activos()
    datos_procesados = []
    
    for indice, p in enumerate(datos_reales, start=1):
        # p[0]=ID_REAL, p[1]=Booster, p[2]=Elo, p[3]=Cuenta, p[4]=Inicio, p[5]=Fin
        id_real = p[0]
        booster = p[1]
        cuenta  = p[3]
        inicio  = p[4]
        fin     = p[5]
        tiempo  = calcular_tiempo_transcurrido(inicio)
        
        datos_procesados.append((indice, id_real, booster, cuenta, inicio, fin, tiempo))
        
    return datos_procesados

def obtener_historial_visual():
    from core.database import obtener_historial
    from core.logic import calcular_duracion_servicio
    
    data = obtener_historial()
    procesados = []
    t = {"booster": 0, "empresa": 0, "cliente": 0}
    
    for i, row in enumerate(data, start=1):
        # row[7] es Inicio, row[8] es Fin
        f_ini_full = row[7]
        f_fin_full = row[8]
        
        # 1. Calculamos la duración ANTES de cortar la hora (para que sea exacto)
        duracion = calcular_duracion_servicio(f_ini_full, f_fin_full)
        
        # 2. Cortamos para mostrar solo FECHA (los primeros 10 caracteres: YYYY-MM-DD)
        f_ini_corta = f_ini_full[:10] if f_ini_full else "N/A"
        f_fin_corta = f_fin_full[:10] if f_fin_full else "N/A"
        
        p_b = row[4] or 0
        g_e = row[5] or 0
        p_c = row[6] or 0
        
        procesados.append((i, row[1], row[2], f"${p_b}", f"${g_e}", f"${p_c}", f_ini_corta, f_fin_corta, duracion))
        
        t["booster"] += p_b
        t["empresa"] += g_e
        t["cliente"] += p_c
        
    return procesados, t
        
    return datos_procesados, totales