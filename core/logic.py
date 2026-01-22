from datetime import datetime, timedelta

# ==========================================
# SECCIÓN 1: NORMALIZACIÓN
# ==========================================

def normalizar_elo(entrada):

    if not entrada: return ""
    texto = entrada.strip().upper()
    mapeo = {
        'D': 'DIAMANTE',
        'P': 'Emerald/Plat',
        'E': 'Emerald/Plat',
        'EP': 'Emerald/Plat'
    }
    return mapeo.get(texto, texto)

# ==========================================
# SECCIÓN 2: LÓGICA FINANCIERA DINÁMICA
# ==========================================

def calcular_pago_real(division, wr, ajuste_manual=0):
    
    from core.database import conectar
    
    division = division.upper().strip()
    conn = conectar()
    cursor = conn.cursor()
    
    try:

        cursor.execute("SELECT precio_cliente, margen_perez FROM config_precios WHERE division = ?", (division,))
        resultado = cursor.fetchone()
        
        if not resultado:
            return 0.0, 0.0, 0.0 # División no encontrada
            
        precio_cliente, margen_perez = resultado
        
        # El pago base del booster es: lo que paga el cliente menos tu ganancia configurada
        pago_booster = precio_cliente - margen_perez
        
        # --- REGLAS DE RENDIMIENTO (HARDCODED POR POLÍTICA) ---
        
        # 1. Bono por excelencia (WR >= 60%)
        if wr >= 60:
            pago_booster += 1.0
            precio_cliente += 1.0 

        # 2. Penalización por bajo rendimiento (WR < 50%)
        # Se le descuenta el 25% de su pago base
        if wr < 50:
            pago_booster -= (pago_booster * 0.25)
        
        # 3. Aplicación de ajustes manuales (Casilla "Otros" en la GUI)
        pago_booster += ajuste_manual
        
        # Aseguramos que el pago no sea negativo
        if pago_booster < 0: pago_booster = 0

        ganancia_final_empresa = precio_cliente - pago_booster
            
        return round(precio_cliente, 2), round(pago_booster, 2), round(ganancia_final_empresa, 2)

    except Exception as e:
        print(f"Error en cálculo financiero: {e}")
        return 0.0, 0.0, 0.0
    finally:
        conn.close()

# ==========================================
# SECCIÓN 3: GESTIÓN DE TIEMPOS
# ==========================================

def calcular_fecha_limite_sugerida(dias=10): 
    return (datetime.now() + timedelta(days=dias)).strftime("%Y-%m-%d %H:%M")

def extender_fecha(fecha_actual_str, dias_a_sumar):
    try:
        fecha_dt = datetime.strptime(fecha_actual_str, "%Y-%m-%d %H:%M")
        nueva = fecha_dt + timedelta(days=dias_a_sumar)
        return nueva.strftime("%Y-%m-%d %H:%M")
    except:
        return None

def calcular_tiempo_transcurrido(fecha_inicio_str):
    try:
        inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M")
        diff = datetime.now() - inicio
        dias, horas = diff.days, diff.seconds // 3600
        
        if dias == 0:
            return f"🟢 Hoy ({horas}h)"
        return f"⚠️ {dias}d {horas}h"
    except: 
        return "N/A"

def calcular_duracion_servicio(f_inicio_str, f_fin_str):
    try:
        inicio = datetime.strptime(f_inicio_str, "%Y-%m-%d %H:%M")
        fin = datetime.strptime(f_fin_str, "%Y-%m-%d %H:%M")
        diff = fin - inicio
        dias, horas = diff.days, diff.seconds // 3600
        
        if dias == 0: return f"{horas}h"
        return f"{dias}d {horas}h"
    except:
        return "N/A"