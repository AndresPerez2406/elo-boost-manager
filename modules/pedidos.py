"""
MÓDULO: GESTIÓN DE PEDIDOS (DURANTE EL SERVICIO)
-----------------------------------------------
Maneja la lógica de visualización y cierre de trabajos activos.
"""
from core.database import obtener_pedidos_activos, obtener_historial
from core.logic import calcular_tiempo_transcurrido, calcular_duracion_servicio

# --- PUENTE PARA GUI ---

def obtener_pedidos_visual():

    datos = obtener_pedidos_activos()
    procesados = []
    
    for p in datos:
        
        tiempo = calcular_tiempo_transcurrido(p[4])
        procesados.append((0, p[0], p[1], p[3], p[4], p[5], tiempo))
        
    return [(i, *p[1:]) for i, p in enumerate(procesados, start=1)]

def obtener_historial_visual():

    datos = obtener_historial()
    procesados = []
    t = {"booster": 0.0, "empresa": 0.0, "cliente": 0.0}
    
    for i, h in enumerate(datos, start=1):
        # id, b_nom, elo_f, wr, pago_b, gan_m, total, f_ini, f_fin
        duracion = calcular_duracion_servicio(h[7], h[8])
        procesados.append((i, h[1], h[2], f"${h[4]}", f"${h[5]}", f"${h[6]}", h[7], h[8], duracion))
        t["booster"] += h[4]; t["empresa"] += h[5]; t["cliente"] += h[6]
        
    return procesados, t

# --- INTERFAZ CMD ---

def menu_pedidos_cli():

    print("\n" + "--- ⚔️ PEDIDOS EN CURSO ---".center(40))
    pedidos = obtener_pedidos_visual()
    if not pedidos:
        print("No hay pedidos activos.")
    else:
        print(f"{'#':<3} | {'BOOSTER':<12} | {'CUENTA':<18} | {'TIEMPO'}")
        print("-" * 50)
        for v, r, b, c, ini, lim, t in pedidos:
            print(f"{v:<3} | {b:<12} | {c[:18]:<18} | {t}")
    input("\nPresiona Enter para volver...")