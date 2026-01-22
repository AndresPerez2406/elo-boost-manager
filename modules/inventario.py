"""
MÓDULO: GESTIÓN DE INVENTARIO (SOPORTE DUAL GUI/CMD)
---------------------------------------------------
Centraliza la lógica de stock de cuentas. Permite registros
individuales, cargas masivas y preparación de datos para tablas.
"""

from core.database import agregar_cuenta, obtener_inventario, eliminar_cuenta

# =========================================================================
#  SECCIÓN 1: PUENTE PARA LA INTERFAZ GRÁFICA (GUI)
# =========================================================================

def obtener_inventario_visual():
    
    try:
        datos_reales = obtener_inventario()
        datos_procesados = []
        
        for indice, fila in enumerate(datos_reales, start=1):

            id_real = fila[0]
            user    = fila[1]
            elo     = fila[2] if fila[2] else "Unranked"
            desc    = fila[3] if fila[3] else "FRESH"
            
      
            datos_procesados.append((indice, id_real, user, elo, desc))
            
        return datos_procesados
    except Exception as e:
        print(f"Error en procesamiento visual de inventario: {e}")
        return []

def registrar_cuenta_gui(u_pass, elo, notas):

    u_pass = u_pass.strip()
    if not u_pass or ":" not in u_pass:
        return False, "❌ Formato inválido. Usa 'Usuario:Password'"
        
    exito = agregar_cuenta(u_pass, elo, notas if notas.strip() else None)
    return exito, "✅ Cuenta guardada" if exito else "❌ Error: Registro fallido (Duplicado?)"

def registrar_lote_gui(texto_masivo, elo):
    
    lineas = texto_masivo.strip().split("\n")
    exitos, errores = 0, 0

    for linea in lineas:
        clean_line = linea.replace("---", ":").replace("    ", ":").strip()
        
        if ":" in clean_line:
            parts = clean_line.split(":")
            if len(parts) >= 2:
                user_pass = f"{parts[0].strip()}:{parts[1].strip()}"
                if agregar_cuenta(user_pass, elo, None):
                    exitos += 1
                    continue
        errores += 1
            
    return exitos, errores

def eliminar_cuenta_gui(id_real):

    return eliminar_cuenta(id_real)


# =========================================================================
# SECCIÓN 2: INTERFAZ DE CONSOLA (EXCLUSIVO CMD)
# =========================================================================

def pedir_elo_cli():

    while True:
        print("\nSelecciona Elo:")
        print(" [D] Diamante | [E/P] Emerald-Plat")
        op = input(">>> (D/E/P): ").strip().upper()
        
        if op == 'D': return 'DIAMANTE'
        if op in ['E', 'P', 'EP']: return 'Emerald/Plat'
        
        print("❌ Opción no válida. Intenta de nuevo.")

def menu_inventario_cli():

    while True:
        print("\n" + "📦 GESTIÓN DE BODEGA (CMD)".center(45, "="))
        print("1. 📋 Ver Stock Disponible")
        print("2. ➕ Agregar Cuenta (Individual)")
        print("3. 📥 Carga Masiva (Lote)")
        print("4. 🗑️ Eliminar Cuenta")
        print("5. 🔙 Volver al Menú Principal")
        print("-" * 45)

        opcion = input(">>> Selecciona: ").strip()

        if opcion == "1":
            stock = obtener_inventario_visual()
            if not stock:
                print("\n   (Bodega vacía)")
            else:
                print(f"\n{'#':<3} | {'ELO':<15} | {'CUENTA':<20} | {'NOTAS'}")
                print("-" * 70)
                for v, r, u, e, n in stock:
                    u_c = (u[:17] + '..') if len(u) > 17 else u
                    print(f"{v:<3} | {e:<15} | {u_c:<20} | {n[:20]}")
            input("\nPresiona Enter para continuar...")

        elif opcion == "2":
            up = input("Usuario:Contraseña: ").strip()
            elo = pedir_elo_cli()
            ex, msg = registrar_cuenta_gui(up, elo, "")
            print(f"\n{msg}")

        elif opcion == "3":
            print("\nPegue las cuentas (User:Pass). Escriba 'FIN' para procesar:")
            lineas = []
            while True:
                l = input()
                if l.upper() == "FIN": break
                if l.strip(): lineas.append(l)
            
            if lineas:
                elo = pedir_elo_cli()
                ex, er = registrar_lote_gui("\n".join(lineas), elo)
                print(f"\n📊 RESUMEN: {ex} Guardadas | {er} Fallidas.")
            input("\nPresiona Enter...")

        elif opcion == "4":
            stock = obtener_inventario_visual()
            print(f"\n{'#':<3} | {'ID_R':<6} | {'CUENTA'}")
            for v, r, u, e, n in stock: 
                print(f"{v:<3} | {r:<6} | {u}")
            
            try:
                id_r = int(input("\nEscribe el ID_R a eliminar: "))
                if eliminar_cuenta_gui(id_r):
                    print("✅ Cuenta eliminada con éxito.")
                else:
                    print("⚠️ No se encontró ese ID.")
            except ValueError:
                print("❌ Entrada inválida.")
            input("\nPresiona Enter...")

        elif opcion == "5":
            break