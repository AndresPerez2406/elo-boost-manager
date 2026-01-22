import os
from core.database import inicializar_db, realizar_backup_db
# Importamos los MENÚS de los módulos
from modules.boosters import menu_boosters_cli
from modules.inventario import menu_inventario_cli
from modules.pedidos import menu_pedidos_cli, obtener_historial_visual

def limpiar(): os.system('cls' if os.name == 'nt' else 'clear')

def menu_principal():
    inicializar_db()
    while True:
        limpiar()
        print("========================================")
        print("🚀 PEREZBOOST MANAGER - CMD EDITION")
        print("========================================")
        print("1. 👥 STAFF (Boosters)")
        print("2. 📦 BODEGA (Inventario)")
        print("3. 📜 TRABAJOS (Pedidos Activos)")
        print("4. 📊 BALANCE (Historial)")
        print("5. 💾 Forzar Backup")
        print("6. ❌ Salir")
        print("----------------------------------------")
        
        op = input(">>> Selecciona: ")
        
        if op == "1":
            menu_boosters_cli() # Menú interactivo completo
        elif op == "2":
            menu_inventario_cli() # Menú interactivo completo
        elif op == "3":
            limpiar()
            menu_pedidos_cli()
        elif op == "4":
            vista_balance_cli()
        elif op == "5":
            realizar_backup_db()
            input("\nBackup completado. Presiona Enter...")
        elif op == "6":
            print("Cerrando sesión. ¡Buen boost!")
            break

def vista_balance_cli():
    limpiar()
    print("==============================================================================================")
    print("📊 HISTORIAL FINANCIERO COMPLETO".center(94))
    print("==============================================================================================")

    from modules.pedidos import obtener_historial_visual
    datos, totales = obtener_historial_visual()

    if not datos:
        print("\n" + "No hay registros en el historial.".center(94))
    else:
        # Encabezados (Iguales a los del GUI)
        header = f"{'#':<3} | {'BOOSTER':<12} | {'ELO/CUENTA':<15} | {'PAGO B.':<10} | {'PEREZ':<10} | {'TOTAL':<10} | {'DURACIÓN'}"
        print(header)
        print("-" * 94)

        # Filas de datos
        for d in datos:
            # d = (indice, booster, elo, pago_b, ganancia_m, total, inicio, fin, duracion)
            print(f"{d[0]:<3} | {d[1]:<12} | {d[2]:<15} | {d[3]:<10} | {d[4]:<10} | {d[5]:<10} | {d[8]}")

    # --- BARRA DE TOTAL (Imitando al GUI) ---
    print("-" * 94)
    print("      TOTAL CALCULADO ".center(94, " "))
    print("-" * 94)
    
    # Formateamos el resumen igual que la barra ancha de la interfaz gráfica
    resumen = f"Boosters: ${totales['booster']:.2f}  |  Ganancia Perez: ${totales['empresa']:.2f}  |  Ingreso Total: ${totales['cliente']:.2f}"
    print(resumen.center(94))
    print("=" * 94)

    input("\nPresiona Enter para volver...")
    
if __name__ == "__main__":
    menu_principal()