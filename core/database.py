import sqlite3
from datetime import datetime

# ==========================================
#  CONFIGURACIÓN Y CONEXIÓN
# ==========================================

def conectar():
    """Establece conexión con la base de datos perezboost.db"""
    return sqlite3.connect("perezboost.db")

def inicializar_db():
    """
    Crea las tablas necesarias con el esquema V6 COMPLETO.
    Incluye campos financieros y de auditoría.
    """
    conn = conectar()
    cursor = conn.cursor()

    # 1. Tabla Boosters
    cursor.execute('''CREATE TABLE IF NOT EXISTS boosters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )''')

    # 2. Tabla Inventario
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_pass TEXT NOT NULL UNIQUE,
            elo_tipo TEXT,
            descripcion TEXT DEFAULT 'FRESH'
        )''')

    # 3. Tabla Pedidos (Esquema Full V6)
    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            
            -- Datos de Asignación
            booster_id INTEGER,
            booster_nombre TEXT, 
            user_pass TEXT,
            elo_inicial TEXT,
            fecha_inicio TEXT,
            fecha_limite TEXT,
            estado TEXT DEFAULT 'En Progreso',
            
            -- Resultados del Trabajo
            elo_final TEXT,
            wr REAL,
            fecha_fin_real TEXT,
            
            -- Datos Financieros
            pago_cliente REAL,
            pago_booster REAL,
            ganancia_empresa REAL,
            
            -- Auditoría y Ajustes Manuales (Casilla "Otros")
            ajuste_valor REAL DEFAULT 0,
            ajuste_motivo TEXT,
            
            FOREIGN KEY (booster_id) REFERENCES boosters (id)
        )''')
    
    conn.commit()
    conn.close()
    print("✅ Base de Datos V6 (Full Schema) inicializada correctamente.")

# ==========================================
#  MÓDULO 1: GESTIÓN DE BOOSTERS
# ==========================================

def agregar_booster(nombre):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO boosters (nombre) VALUES (?)", (nombre,))
        conn.commit()
        print(f"✅ Booster '{nombre}' registrado.")
        exito = True
    except sqlite3.IntegrityError:
        print(f"❌ El booster '{nombre}' ya existe.")
        exito = False
    finally:
        conn.close()
    return exito

def obtener_boosters_db():
    """Retorna todos los boosters de la tabla boosters (corregido)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre FROM boosters") 
    data = cursor.fetchall()
    conn.close()
    return data

def eliminar_booster(id_booster):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM boosters WHERE id = ?", (id_booster,))
    exito = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return exito

# ==========================================
#  MÓDULO 2: GESTIÓN DE INVENTARIO
# ==========================================

def agregar_cuenta(user_pass, elo_tipo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO inventario (user_pass, elo_tipo) VALUES (?, ?)", (user_pass, elo_tipo))
        conn.commit()
        print(f"✅ Cuenta guardada: {user_pass} ({elo_tipo})")
        exito = True
    except sqlite3.IntegrityError:
        print(f"⚠️ Cuenta duplicada o error de integridad.")
        exito = False
    finally:
        conn.close()
    return exito

def obtener_inventario():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_pass, elo_tipo, descripcion FROM inventario ORDER BY elo_tipo")
    items = cursor.fetchall()
    conn.close()
    return items

def eliminar_cuenta(id_cuenta):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventario WHERE id = ?", (id_cuenta,))
    exito = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return exito

def actualizar_estructura_inventario():
    """Añade la columna descripcion si no existe."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Intentamos añadir la columna con valor por defecto 'FRESH'
        cursor.execute("ALTER TABLE inventario ADD COLUMN descripcion TEXT DEFAULT 'FRESH'")
        conn.commit()
    except:
        # Si ya existe, no hará nada
        pass
    finally:
        conn.close()
        
def registrar_abandono_db(id_pedido, elo_dejado, wr_dejado):
    
    conn = conectar()
    cursor = conn.cursor()
    exito = False
    
    try:
        # 1. Recuperar info del pedido original
        cursor.execute("SELECT user_pass, elo_inicial FROM pedidos WHERE id = ?", (id_pedido,))
        datos = cursor.fetchone()
        
        if not datos:
            print(f"❌ Error DB: El pedido ID {id_pedido} no existe.")
            return False
            
        u_p, elo_orig = datos
        fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # ---------------------------------------------------------------
        # 🧠 LÓGICA SIMPLIFICADA (LO QUE PEDISTE)
        # ---------------------------------------------------------------
        
        # 1. El Tipo de Elo vuelve a ser EXACTAMENTE el que era antes (elo_orig)
        #    Si la cuenta era "DIAMANTE", vuelve como "DIAMANTE".
        categoria_inv = elo_orig 
        
        # 2. Los datos nuevos van SOLO a la descripción
        nota = f"⚠️ ABANDONO. Dejada en: {elo_dejado} ({wr_dejado}% WR)"
        
        # ---------------------------------------------------------------

        # 2. Devolver al inventario
        try:
            cursor.execute("""
                INSERT INTO inventario (user_pass, elo_tipo, descripcion)
                VALUES (?, ?, ?)
            """, (u_p, categoria_inv, nota))
            
        except sqlite3.IntegrityError:
            print("   (La cuenta ya existía, restaurando tipo original y actualizando nota...)")
            # Si ya existe, forzamos que el tipo sea el original y actualizamos la nota
            cursor.execute("""
                UPDATE inventario 
                SET elo_tipo = ?, descripcion = ? 
                WHERE user_pass = ?
            """, (categoria_inv, nota, u_p))

        # 3. Cerrar el pedido como 'Abandonado'
        cursor.execute("""
            UPDATE pedidos 
            SET estado = 'Abandonado',
                elo_final = ?,
                wr = ?,
                fecha_fin_real = ?,
                ganancia_empresa = 0,
                pago_booster = 0
            WHERE id = ?
        """, (elo_dejado, wr_dejado, fecha_fin, id_pedido))
        
        conn.commit()
        exito = True
        
        print("\n" + "-"*40)
        print(f"✅ REPORTE EXITOSO")
        print(f"📦 Tipo Restaurado:     {categoria_inv}")
        print(f"📝 Nota Agregada:       {nota}")
        print("-"*40 + "\n")

    except Exception as e:
        conn.rollback()
        print(f"\n🔥 ERROR TÉCNICO EN DB: {e}") 
        
    finally:
        conn.close()
    
    return exito

# ==========================================
#  MÓDULO 3: GESTIÓN DE PEDIDOS (CORE)
# ==========================================

def obtener_cuentas_disponibles_por_elo(tipo_elo):
    """Busca cuentas ignorando mayúsculas/minúsculas y trayendo la descripción."""
    conn = conectar()
    cursor = conn.cursor()
    # Usamos UPPER para que 'diamante' y 'DIAMANTE' sean lo mismo
    query = """
        SELECT id, user_pass, descripcion
        FROM inventario
        WHERE UPPER(TRIM(elo_tipo)) = UPPER(TRIM(?))
    """
    cursor.execute(query, (tipo_elo,))
    cuentas = cursor.fetchall()
    conn.close()
    return cuentas

def crear_pedido(id_booster, nombre_booster, id_cuenta, user_pass, elo, fecha_fin):
    """
    TRANSACTION: Mueve una cuenta del Inventario -> Pedidos.
    FIX: Ahora inserta el estado 'En progreso' correctamente.
    """
    conn = conectar()
    cursor = conn.cursor()
    exito = False
    
    try:
        fecha_hoy = datetime.now().strftime("%Y-%m-%d %H:%M")
        
        # Agregamos 'estado' a la lista de columnas y 'En progreso' a los valores
        cursor.execute('''
            INSERT INTO pedidos (
                booster_id, booster_nombre, user_pass, elo_inicial, 
                fecha_inicio, fecha_limite, estado
            )
            VALUES (?, ?, ?, ?, ?, ?, 'En progreso')
        ''', (id_booster, nombre_booster, user_pass, elo, fecha_hoy, fecha_fin))

        # 2. Eliminamos del Inventario
        cursor.execute("DELETE FROM inventario WHERE id = ?", (id_cuenta,))

        conn.commit()
        print(f"✅ Pedido asignado a {nombre_booster} [En progreso].")
        exito = True

    except Exception as e:
        conn.rollback() 
        print(f"❌ Error CRÍTICO en la transacción: {e}")
    
    finally:
        conn.close()
    
    return exito

def obtener_pedidos_activos():
    """Retorna todos los pedidos que están actualmente en curso."""
    conn = conectar()
    cursor = conn.cursor()
    query = """
        SELECT id, booster_nombre, elo_inicial, user_pass, fecha_inicio, fecha_limite 
        FROM pedidos 
        WHERE estado = 'En progreso'
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

def obtener_pedido_por_id(id_pedido):
    """Busca un pedido específico para operaciones de edición (como extender plazo)."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fecha_limite FROM pedidos WHERE id = ?", (id_pedido,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def obtener_boosters_activos_db():
    """Retorna lista de boosters que tienen al menos un pedido 'En progreso'."""
    conn = conectar()
    cursor = conn.cursor()
    query = '''
        SELECT DISTINCT b.id, b.nombre 
        FROM boosters b
        JOIN pedidos p ON b.id = p.booster_id
        WHERE p.estado = 'En progreso'
    '''
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_pedidos_por_booster_id(id_booster_seleccionado):
    """Filtra todos los trabajos activos de un booster específico."""
    conn = conectar()
    cursor = conn.cursor()
    
    # ERROR CORREGIDO 3: No hacemos JOIN con cuentas, porque en tu lógica V6 
    # guardaste el user_pass y el elo directamente en la tabla pedidos.
    query = '''
        SELECT id, booster_nombre, elo_inicial, user_pass, fecha_inicio, fecha_limite
        FROM pedidos
        WHERE booster_id = ? AND estado = 'En progreso'
    '''
    cursor.execute(query, (id_booster_seleccionado,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def actualizar_fecha_limite_db(id_pedido, nueva_fecha):
    """Actualiza el deadline en la base de datos."""
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE pedidos SET fecha_limite = ? WHERE id = ?", (nueva_fecha, id_pedido))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error al actualizar fecha: {e}")
        return False
    finally:
        conn.close()

# ==========================================
#  MÓDULO 4: CIERRE Y FINANZAS
# ==========================================

def finalizar_pedido_db(id_pedido, elo_final, wr, cobro, pago_b, ganancia, ajuste_v, ajuste_m):
    """
    Cierra el pedido guardando toda la auditoría financiera.
    """
    conn = conectar()
    cursor = conn.cursor()
    fecha_fin = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    try:
        # Fíjate que hay 8 campos en el SET + 1 en el WHERE = 9 signos de interrogación (?)
        cursor.execute("""
            UPDATE pedidos 
            SET estado = 'Terminado',
                elo_final = ?,
                wr = ?,
                pago_cliente = ?,
                pago_booster = ?,
                ganancia_empresa = ?,
                fecha_fin_real = ?,
                ajuste_valor = ?,
                ajuste_motivo = ?
            WHERE id = ?
        """, (elo_final, wr, cobro, pago_b, ganancia, fecha_fin, ajuste_v, ajuste_m, id_pedido))
        # ^^^ Aquí contamos: 1, 2, 3, 4, 5, 6, 7, 8, 9. ¡Ahora sí cuadra!
        
        conn.commit()
        exito = True
    except Exception as e:
        print(f"❌ Error CRÍTICO al guardar en DB: {e}")
        exito = False
    finally:
        conn.close()
    return exito

def obtener_historial():
    conn = conectar()
    cursor = conn.cursor()
    # Se añade fecha_inicio para el cálculo de eficiencia
    query = """
        SELECT id, booster_nombre, elo_final, wr, pago_booster, ganancia_empresa, 
               pago_cliente, fecha_inicio, fecha_fin_real 
        FROM pedidos 
        WHERE estado = 'Terminado'
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data
    return data