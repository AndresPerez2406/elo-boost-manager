"""
MÓDULO: GESTIÓN DE PEDIDOS (DURANTE EL SERVICIO)
-----------------------------------------------
Maneja la lógica de visualización y cierre de trabajos activos.
"""
from core.database import (
    obtener_pedidos_activos, 
    obtener_historial, 
    conectar, 
    obtener_boosters_db as db_get_boosters
)
from core.logic import calcular_tiempo_transcurrido, calcular_duracion_servicio

# ======================================================
#  PUENTE PARA GUI Y LÓGICA VISUAL
# ======================================================

def obtener_pedidos_visual():
    """
    Procesa los pedidos activos para mostrarlos en tablas (GUI/CMD).
    Calcula el tiempo transcurrido usando core.logic.
    """
    datos = obtener_pedidos_activos()
    procesados = []
    
    for p in datos:
        # p = (id, booster_nombre, elo_inicial, user_pass, fecha_inicio, fecha_limite)
        tiempo = calcular_tiempo_transcurrido(p[4])
        
        # Estructura intermedia: (dummy_index, id_real, booster, cuenta, inicio, fin, tiempo)
        procesados.append((0, p[0], p[1], p[3], p[4], p[5], tiempo))
        
    # Retorna: (Índice Visual, ID_Real, Booster, Cuenta, Inicio, Fin, Tiempo)
    return [(i, *p[1:]) for i, p in enumerate(procesados, start=1)]

def obtener_historial_visual():
    """
    Procesa el historial terminado y calcula totales financieros.
    """
    datos = obtener_historial()
    procesados = []
    t = {"booster": 0.0, "empresa": 0.0, "cliente": 0.0}
    
    for i, h in enumerate(datos, start=1):
        # h = (id, b_nom, elo_f, wr, pago_b, gan_m, total, f_ini, f_fin)
        duracion = calcular_duracion_servicio(h[7], h[8])
        
        # Formato para tabla: (#, Booster, Elo, PagoB, Ganancia, Total, Inicio, Fin, Duración)
        procesados.append((i, h[1], h[2], f"${h[4]}", f"${h[5]}", f"${h[6]}", h[7], h[8], duracion))
        
        # Sumar totales (validando que no sean None)
        t["booster"] += h[4] if h[4] else 0
        t["empresa"] += h[5] if h[5] else 0
        t["cliente"] += h[6] if h[6] else 0
        
    # Retornamos la lista y una tupla con los totales
    return procesados, (t["booster"], t["empresa"], t["cliente"])

# ======================================================
#  INTERFAZ CMD (TEXTO)
# ======================================================

def menu_pedidos_cli():
    print("\n" + "--- ⚔️ PEDIDOS EN CURSO ---".center(40))
    pedidos = obtener_pedidos_visual()
    if not pedidos:
        print("No hay pedidos activos.")
    else:
        # v=visual_id, r=real_id, b=booster, c=cuenta, ini=inicio, lim=limite, t=tiempo
        print(f"{'#':<3} | {'BOOSTER':<12} | {'CUENTA':<18} | {'TIEMPO'}")
        print("-" * 50)
        for v, r, b, c, ini, lim, t in pedidos:
            print(f"{v:<3} | {b:<12} | {c[:18]:<18} | {t}")
    input("\nPresiona Enter para volver...")

# ======================================================
#  FUNCIONES AUXILIARES OBLIGATORIAS PARA LA GUI
#  (Sin estas, el botón 'Nuevo Pedido' da error)
# ======================================================

def obtener_elos_en_stock():
    """Retorna lista de Elos disponibles (ej: ['D1', 'P4']) para el combobox."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT elo_tipo FROM inventario ORDER BY elo_tipo")
    resultados = cursor.fetchall()
    conn.close()
    return [r[0] for r in resultados] if resultados else []

def obtener_cuentas_filtradas_datos(elo_seleccionado):
    """Retorna las cuentas específicas de un Elo para llenar el segundo combobox."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_pass, descripcion FROM inventario WHERE elo_tipo = ?", (elo_seleccionado,))
    data = cursor.fetchall()
    conn.close()
    return data

def obtener_boosters_db():
    """Wrapper para mantener compatibilidad de nombres en la importación."""
    return db_get_boosters()