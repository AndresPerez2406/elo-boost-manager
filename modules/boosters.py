"""
MÓDULO: GESTIÓN DE BOOSTERS (SOPORTE DUAL GUI/CMD)
-------------------------------------------------
Este módulo centraliza la lógica del staff. Las funciones de 'logica' 
devuelven datos, mientras que las de 'cli' manejan la interacción de consola.
"""

from core.database import agregar_booster, obtener_boosters_db, eliminar_booster

# =========================================================================
#  SECCIÓN 1: LÓGICA DE NEGOCIO (COMPARTIDA)
# =========================================================================

def registrar_booster_logica(nombre_entrada):

    nombre_limpio = nombre_entrada.strip().title()

    if not nombre_limpio:
        return False, "⚠️ El nombre no puede estar vacío."

    if len(nombre_limpio) < 3:
        return False, "⚠️ El nombre es demasiado corto (mínimo 3 letras)."

    if agregar_booster(nombre_limpio):
        return True, f"✅ '{nombre_limpio}' registrado exitosamente."
    else:
        return False, f"❌ El booster '{nombre_limpio}' ya existe."

def obtener_boosters_procesados():

    try:
        datos_raw = obtener_boosters_db()
       
        return [(i, b[0], b[1]) for i, b in enumerate(datos_raw, start=1)]
    except Exception as e:
        print(f"Error en lectura de boosters: {e}")
        return []

def eliminar_booster_logica(id_real):

    if eliminar_booster(id_real):
        return True, "✅ Booster eliminado correctamente."
    else:
        return False, "❌ Error: No se encontró el registro."

# =========================================================================
#  SECCIÓN 2: INTERFAZ DE CONSOLA (EXCLUSIVO CMD)
# =========================================================================

def menu_boosters_cli():

    while True:
        print("\n" + "--- 👥 GESTIÓN DE STAFF ---".center(30))
        print("1. Ver lista de Boosters")
        print("2. Agregar Nuevo")
        print("3. Eliminar por ID")
        print("4. Volver")
        
        op = input(">>> Selecciona: ").strip()

        if op == "1":
            staff = obtener_boosters_procesados()
            print(f"\n{'#':<3} | {'NOMBRE':<20}")
            print("-" * 25)
            for v_id, r_id, nombre in staff:
                print(f"{v_id:<3} | {nombre}")
            input("\nPresiona Enter para continuar...")

        elif op == "2":
            nombre = input("Nombre del Booster: ")
            exito, msg = registrar_booster_logica(nombre)
            print(msg)

        elif op == "3":

            staff = obtener_boosters_procesados()
            print(f"\n{'#':<3} | {'ID_REAL':<8} | {'NOMBRE'}")
            for v_id, r_id, nombre in staff:
                print(f"{v_id:<3} | {r_id:<8} | {nombre}")
            
            try:
                id_target = int(input("\nEscribe el ID_REAL a eliminar: "))
                exito, msg = eliminar_booster_logica(id_target)
                print(msg)
            except ValueError:
                print("❌ ID inválido.")

        elif op == "4":
            break