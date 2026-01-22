import os
from core.database import inicializar_db, actualizar_estructura_inventario
from modules.boosters import menu_boosters
from modules.inventario import menu_inventario
from modules.pedidos import menu_pedidos

def main():
    # 1. Aseguramos que la DB exista
    inicializar_db()
    
    # 2. Parcheamos la estructura por si faltan columnas nuevas (Auto-Repair)
    actualizar_estructura_inventario()

    while True:
        # Limpiador de pantalla opcional (Descoméntalo para un look más limpio)
        # os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\n" + "█"*40)
        print("   PEREZBOOST MANAGER v6 (SQL EDITION)")
        print("█"*40)
        print("1. 👥 Gestión de Boosters")
        print("2. 📦 Inventario")
        print("3. 📝 Pedidos")
        print("4. 🚪 Salir")

        op = input("\n>>> Selecciona: ")

        if op == "1":
            menu_boosters()
        elif op == "2":
            menu_inventario()
        elif op == "3":
            menu_pedidos()
        elif op == "4":
            print("👋 ¡Nos vemos, Manager!")
            break
        
if __name__ == "__main__":
    main()