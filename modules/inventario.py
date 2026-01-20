from core.database import agregar_cuenta, obtener_inventario, eliminar_cuenta
from core.database import obtener_inventario

def menu_inventario():
    while True:
        print("\n" + "📦 GESTIÓN DE BODEGA V6".center(40, "="))
        print("1. 📋 Ver Stock Disponible")
        print("2. ➕ Agregar Cuenta (Individual)")
        print("3. 📥 Agregar Lote (Masivo)")
        print("4. 🗑️ Eliminar Cuenta")
        print("5. 🔙 Volver")

        opcion = input(">>> Selecciona: ").strip()

        if opcion == "1":
            mostrar_stock()

        elif opcion == "2":
            agregar_individual()

        elif opcion == "3":
            agregar_masivo()

        elif opcion == "4":
            mostrar_stock()
            try:
                id_del = int(input("\nID de la cuenta a eliminar: "))
                if eliminar_cuenta(id_del):
                    print("✅ Cuenta eliminada.")
                else:
                    print("⚠️ ID no encontrado.")
            except ValueError:
                print("❌ ID inválido.")

        elif opcion == "5":
            break

def mostrar_stock():
    
    print("\n" + "--- 📦 INVENTARIO COMPLETO ---".center(85))
    
    # Llamamos a core/database.py
    stock = obtener_inventario()
    
    if not stock:
        print("   (La bodega está vacía 🕸️)".center(85))
        return

    # Header: Usamos '#' para el ID Visual
    # Mantengo el ID Real en el empaquetado por si lo necesitas, pero no lo imprimimos
    print(f"{'#':<4} | {'TIPO':<17} | {'CUENTA':<20} | {'NOTAS / ESTADO'}")
    print("-" * 85)

    # USAMOS ENUMERATE para el ID Visual (1, 2, 3...)
    for i, item in enumerate(stock, start=1):
        # item[0]=id_real, item[1]=user, item[2]=elo, item[3]=descripcion
        id_real = item[0]
        up      = item[1]
        elo     = item[2] if item[2] else "Unranked"
        nota    = item[3] if item[3] else "FRESH"

        # Formateo de usuario
        up_clean = (up[:18] + '..') if len(up) > 18 else up
        
        # IMPRIMIMOS EL ÍNDICE 'i' (ID Visual) en lugar de 'id_real'
        print(f"{i:<4} | {elo:<17} | {up_clean:<20} | {nota}")

    print("-" * 85)

def agregar_individual():
    print("\n--- AGREGAR CUENTA ÚNICA ---")
    u_pass = input("Usuario:Contraseña: ").strip()
    
    # Limpieza básica
    if ":" in u_pass:
        parts = u_pass.split(":")
        u_pass = f"{parts[0].strip()}:{parts[1].strip()}"
    
    elo = pedir_elo()
    if elo:
        agregar_cuenta(u_pass, elo)

def agregar_masivo():
    print("\n--- IMPORTACIÓN MASIVA ---")
    print("Pegue su lista de cuentas (USER:PASS).")
    print("Escriba 'FIN' en una nueva línea para terminar.")
    print("-" * 30)

    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":
            break
        if linea.strip(): 
            lineas.append(linea)
    
    if not lineas:
        return

    print(f"\nRecibidas {len(lineas)} líneas.")
    elo_lote = pedir_elo()
    if not elo_lote: return

    print("\n... Procesando ...")
    exitos = 0
    errores = 0

    for linea in lineas:
        clean_line = linea.replace("----", ":").replace("    ", ":")
        
        if ":" in clean_line:
            parts = clean_line.split(":")
            if len(parts) >= 2:
                final_cred = f"{parts[0].strip()}:{parts[1].strip()}"
                if agregar_cuenta(final_cred, elo_lote):
                    exitos += 1
                else:
                    errores += 1
            else:
                errores += 1
        else:
            errores += 1

    print(f"\n📊 RESUMEN: {exitos} guardadas | {errores} fallidas.")

def pedir_elo():
    """
    Valida y estandariza el Elo.
    REGLA: Solo acepta D, E, P. Cualquier otra letra se rechaza.
    """
    while True:
        print("\nSelecciona Elo:")
        print(" [D]   = Diamante")
        print(" [E/P] = Emerald / Plat")
        
        # .upper() convierte 'd' en 'D' automáticamente
        elo = input(">>> Tipo (D, E, P): ").strip().upper()
        
        if elo == 'D':
            return 'DIAMANTE'
            
        elif elo in ['EP', 'E', 'P']: 
            # Estandarizamos E y P bajo el nombre exacto que pediste
            return 'Emerald/Plat'
            
        else:
            # Aquí está el filtro: Si no es D, E o P, no avanza.
            print("❌ Opción no válida. Solo guardamos Diamante (D) o Emerald/Plat (E/P).")
            print("   Intenta de nuevo.")

def obtener_inventario_visual():
    """Trae datos de SQL y genera (ID_VISUAL, ID_REAL, USER, ELO, DESC)"""
    datos_reales = obtener_inventario()
    datos_procesados = []
    
    for indice, fila in enumerate(datos_reales, start=1):
        # fila[0]=id_real, fila[1]=user, fila[2]=elo, fila[3]=desc
        id_real = fila[0]
        user = fila[1]
        elo = fila[2] if fila[2] else "Unranked"
        desc = fila[3] if fila[3] else "FRESH"
        
        # Guardamos la tupla con los 5 elementos que la GUI espera
        datos_procesados.append((indice, id_real, user, elo, desc))
        
    return datos_procesados