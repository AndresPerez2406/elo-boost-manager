import sqlite3
import os
import shutil
from datetime import datetime

# ==========================================
# SECCIÓN 0: CONFIGURACIÓN Y BACKUP
# ==========================================

def conectar():

    return sqlite3.connect("perezboost.db")

def realizar_backup_db():
    archivo_db = "perezboost.db"
    carpeta_backups = "backups"
    
    if not os.path.exists(archivo_db): return 
    if not os.path.exists(carpeta_backups): os.makedirs(carpeta_backups)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_destino = os.path.join(carpeta_backups, f"backup_{timestamp}.db")

    try:
        shutil.copy2(archivo_db, ruta_destino)
        gestionar_limite_backups(carpeta_backups)
        print(f"📦 Backup automático creado.")
    except Exception as e:
        print(f"❌ Error en backup: {e}")

def gestionar_limite_backups(ruta_carpeta, limite=10):
    archivos = [os.path.join(ruta_carpeta, f) for f in os.listdir(ruta_carpeta)]
    archivos.sort(key=os.path.getmtime)
    while len(archivos) > limite:
        os.remove(archivos.pop(0))

def inicializar_db():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS boosters (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY AUTOINCREMENT, user_pass TEXT NOT NULL UNIQUE, elo_tipo TEXT, descripcion TEXT DEFAULT "FRESH")')
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT, booster_id INTEGER, booster_nombre TEXT, 
            user_pass TEXT, elo_inicial TEXT, fecha_inicio TEXT, fecha_limite TEXT, 
            estado TEXT DEFAULT 'En progreso', elo_final TEXT, wr REAL, fecha_fin_real TEXT,
            pago_cliente REAL, pago_booster REAL, ganancia_empresa REAL, ajuste_valor REAL DEFAULT 0, ajuste_motivo TEXT,
            FOREIGN KEY (booster_id) REFERENCES boosters (id))''')
    
    cursor.execute('CREATE TABLE IF NOT EXISTS config_precios (division TEXT PRIMARY KEY, precio_cliente REAL, margen_perez REAL)')

    cursor.execute("SELECT COUNT(*) FROM config_precios")
    if cursor.fetchone()[0] == 0:
        precios = [('D1', 45.0, 10.0), ('D2', 35.0, 10.0), ('D3', 30.0, 10.0), ('D4', 30.0, 10.0),
                   ('E1', 18.0, 5.0), ('E2', 15.0, 5.0), ('E3', 12.0, 5.0), ('E4', 12.0, 5.0),
                   ('P1', 10.0, 5.0), ('P2', 10.0, 5.0), ('P3', 8.0, 5.0), ('P4', 8.0, 5.0)]
        cursor.executemany("INSERT INTO config_precios VALUES (?, ?, ?)", precios)
    
    conn.commit()
    conn.close()

# ==========================================
# SECCIÓN 1: GESTIÓN DE BOOSTERS
# ==========================================

def agregar_booster(nombre):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO boosters (nombre) VALUES (?)", (nombre,))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def obtener_boosters_db():
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM boosters") 
    data = cursor.fetchall(); conn.close(); return data

def eliminar_booster(id_booster):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM boosters WHERE id = ?", (id_booster,))
    exito = cursor.rowcount > 0
    conn.commit(); conn.close(); return exito

# ==========================================
# SECCIÓN 2: GESTIÓN DE INVENTARIO
# ==========================================

def agregar_cuenta(user_pass, elo_tipo, descripcion=None):
    if not descripcion or str(descripcion).strip() == "": descripcion = "FRESH"
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventario (user_pass, elo_tipo, descripcion) VALUES (?, ?, ?)", (user_pass, elo_tipo, descripcion))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def obtener_inventario():
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT id, user_pass, elo_tipo, descripcion FROM inventario ORDER BY elo_tipo")
    items = cursor.fetchall(); conn.close(); return items

def eliminar_cuenta(id_cuenta):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("DELETE FROM inventario WHERE id = ?", (id_cuenta,))
    exito = cursor.rowcount > 0; conn.commit(); conn.close(); return exito

# ==========================================
# SECCIÓN 3: GESTIÓN DE PEDIDOS
# ==========================================

def crear_pedido(id_booster, nombre_booster, id_cuenta, user_pass, elo, fecha_fin):
    conn = conectar(); cursor = conn.cursor(); exito = False
    try:
        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute('''INSERT INTO pedidos (booster_id, booster_nombre, user_pass, elo_inicial, 
                          fecha_inicio, fecha_limite, estado) VALUES (?, ?, ?, ?, ?, ?, 'En progreso')''', 
                       (id_booster, nombre_booster, user_pass, elo, fecha_hoy, fecha_fin))
        cursor.execute("DELETE FROM inventario WHERE id = ?", (id_cuenta,))
        conn.commit(); exito = True
    except: conn.rollback()
    finally: conn.close(); 
    
    return exito

def obtener_pedidos_activos():
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT id, booster_nombre, elo_inicial, user_pass, fecha_inicio, fecha_limite FROM pedidos WHERE estado = 'En progreso'")
    data = cursor.fetchall(); conn.close(); return data

def registrar_abandono_db(id_pedido, elo_dejado, wr_dejado):
    conn = conectar(); cursor = conn.cursor(); exito = False
    try:
        cursor.execute("SELECT user_pass, elo_inicial FROM pedidos WHERE id = ?", (id_pedido,))
        datos = cursor.fetchone()
        if not datos: return False
        u_p, elo_orig = datos
        fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M")
        nota = f"⚠️ ABANDONO. Dejada en: {elo_dejado} ({wr_dejado}% WR)"
        cursor.execute("INSERT INTO inventario (user_pass, elo_tipo, descripcion) VALUES (?, ?, ?) ON CONFLICT(user_pass) DO UPDATE SET elo_tipo=?, descripcion=?", (u_p, elo_orig, nota, elo_orig, nota))
        cursor.execute("UPDATE pedidos SET estado='Abandonado', elo_final=?, wr=?, fecha_fin_real=? WHERE id=?", (elo_dejado, wr_dejado, fecha_fin, id_pedido))
        conn.commit(); exito = True
    finally: conn.close(); 
    
    return exito

# ==========================================
# SECCIÓN 4: FINANZAS E HISTORIAL
# ==========================================

def finalizar_pedido_db(id_pedido, elo_final, wr, cobro, pago_b, ganancia, ajuste_v, ajuste_m):
    conn = conectar(); cursor = conn.cursor(); fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M")
    try:
        cursor.execute("""UPDATE pedidos SET estado = 'Terminado', elo_final = ?, wr = ?, 
                          pago_cliente = ?, pago_booster = ?, ganancia_empresa = ?, 
                          fecha_fin_real = ?, ajuste_valor = ?, ajuste_motivo = ? WHERE id = ?""", 
                       (elo_final, wr, cobro, pago_b, ganancia, fecha_fin, ajuste_v, ajuste_m, id_pedido))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def obtener_historial():
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("""SELECT id, booster_nombre, elo_final, wr, pago_booster, ganancia_empresa, 
                      pago_cliente, fecha_inicio, fecha_fin_real FROM pedidos WHERE estado = 'Terminado'""")
    data = cursor.fetchall(); conn.close(); return data

# ==========================================
# SECCIÓN 5: CONFIGURACIÓN DE TARIFAS
# ==========================================

def obtener_config_precios():
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("SELECT division, precio_cliente, margen_perez FROM config_precios ORDER BY division ASC")
    res = cursor.fetchall(); conn.close(); return res

def actualizar_precio_db(div, p_cli, m_per):
    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("UPDATE config_precios SET precio_cliente = ?, margen_perez = ? WHERE division = ?", (p_cli, m_per, div))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def agregar_precio_db(div, p_cli, m_per):

    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO config_precios (division, precio_cliente, margen_perez) VALUES (?, ?, ?)", (div, p_cli, m_per))
        conn.commit(); return True
    except: return False
    finally: conn.close()

def eliminar_precio_db(div):

    conn = conectar(); cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM config_precios WHERE division = ?", (div,))
        exito = cursor.rowcount > 0
        conn.commit(); return exito
    except: return False
    finally: conn.close()