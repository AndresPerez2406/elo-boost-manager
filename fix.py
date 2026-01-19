import sqlite3
import os

# Buscamos la base de datos (igual que en main.py)
DB_PATH = "perezboost.db"
if not os.path.exists(DB_PATH):
    # Por si acaso está en otra carpeta
    DB_PATH = os.path.join("core", "perezboost.db")

def corregir_nombres_elo():
    print(f"🔧 Conectando a la base de datos: {DB_PATH}...")
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 1. VERIFICAR: ¿Cuántas cuentas tienen el nombre viejo?
        cursor.execute("SELECT COUNT(*) FROM inventario WHERE elo_tipo = 'ESMERALDA/PLATINO'")
        cantidad_viejas = cursor.fetchone()[0]

        if cantidad_viejas == 0:
            print("\n✅ ¡Todo limpio! No encontré ninguna cuenta con el nombre antiguo.")
            return

        print(f"\n⚠️ Se encontraron {cantidad_viejas} cuentas llamadas 'ESMERALDA/PLATINO'.")
        print("   Se cambiarán a: 'Emerald/Plat'")
        
        if input("¿Proceder con el cambio? (S/N): ").upper() == "S":
            # 2. EJECUTAR EL CAMBIO (UPDATE)
            cursor.execute("""
                UPDATE inventario 
                SET elo_tipo = 'Emerald/Plat' 
                WHERE elo_tipo = 'ESMERALDA/PLATINO'
            """)
            
            conn.commit()
            cambios = cursor.rowcount
            print(f"\n✨ ¡ÉXITO! Se actualizaron {cambios} cuentas.")
            
            # Verificación final
            cursor.execute("SELECT COUNT(*) FROM inventario WHERE elo_tipo = 'Emerald/Plat'")
            nuevas = cursor.fetchone()[0]
            print(f"   Total actual de 'Emerald/Plat': {nuevas}")
            
        else:
            print("Operación cancelada.")

    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals(): conn.close()

if __name__ == "__main__":
    corregir_nombres_elo()