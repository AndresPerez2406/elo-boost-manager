from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE PRECIOS Y TRADUCCIÓN ---

PRECIOS_BASE = {
    "D4": 30, "D3": 30, "D2": 35, "D1": 45,
    "E4": 12, "E3": 12, "E2": 15, "E1": 18,
    "P4": 8,  "P3": 8,  "P2": 10, "P1": 10,
    "G4": 5,  "G3": 5,  "G2": 5,  "G1": 5  # Agregué Oro por si acaso
}

MARGEN_GANANCIA = { "D": 10.0, "E": 5.0, "P": 5.0, "G": 2.0 }

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

# --- 2. LÓGICA DE DINERO ---

def calcular_pago_real(division, wr, ajuste_manual=0):
    division = division.upper().strip()
    
    # Si la división no tiene precio, retornamos ceros
    if division not in PRECIOS_BASE:
        return 0, 0, 0
    
    precio_cliente = float(PRECIOS_BASE[division])
    tipo_elo = division[0] # D, E, P, G
    mi_ganancia_base = MARGEN_GANANCIA.get(tipo_elo, 5.0)
    
    pago_booster = precio_cliente - mi_ganancia_base
    
    # Regla: Bono WR >= 60%
    if wr >= 60:
        pago_booster += 1.0
        precio_cliente += 1.0 

    # Regla: Penalización WR < 50%
    if wr < 50:
        pago_booster -= (pago_booster * 0.25)
    
    pago_booster += ajuste_manual
    if pago_booster < 0: pago_booster = 0

    ganancia_empresa = precio_cliente - pago_booster
        
    return round(precio_cliente, 2), round(pago_booster, 2), round(ganancia_empresa, 2)

# --- 3. LÓGICA DE FECHAS ---

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
    except: return "N/A"

def calcular_duracion_boost(inicio_str, fin_str):
    return "N/A" # Simplificado