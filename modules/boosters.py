from core.database import agregar_booster, obtener_boosters_db, eliminar_booster

def menu_boosters():
    """Menú interactivo para gestionar el equipo."""
    while True:
        print("\n--- 👥 GESTIÓN DE EQUIPO (SQL VERSION) ---")
        print("1. Ver lista de Boosters")
        print("2. Contratar (Agregar Nuevo)")
        print("3. Despedir (Eliminar)")
        print("4. Volver al Menú Principal")
        
        opcion = input(">>> Selecciona: ").strip()

        if opcion == "1":
            mostrar_lista()
        
        elif opcion == "2":
            nombre = input("Nombre del nuevo Booster: ").strip().title()
            if nombre:
                # Llamamos a la capa de datos (core)
                agregar_booster(nombre)
            else:
                print("⚠️ El nombre no puede estar vacío.")

        elif opcion == "3":
            mostrar_lista()
            try:
                id_eliminar = int(input("\nEscribe el ID del booster a eliminar: "))
                # Guardamos el resultado para confirmar
                if eliminar_booster(id_eliminar):
                    print("✅ Booster eliminado de la base de datos.")
                else:
                    print("❌ No se encontró ningún booster con ese ID.")
            except ValueError:
                print("❌ Debes escribir un número válido (ID).")

        elif opcion == "4":
            break
        else:
            print("❌ Opción no válida.")

def mostrar_lista():
    """Función auxiliar para formatear la salida."""
    boosters = obtener_boosters_db()
    
    if not boosters:
        print("\n   (La nómina está vacía. ¡Contrata a alguien!)")
    else:
        print("\n   ID | NOMBRE")
        print("   " + "-"*15)
        for id_b, nombre in boosters:
            # f-strings para alinear texto (ID ocupa 3 espacios, Nombre el resto)
            print(f"   {id_b:<3}| {nombre}")