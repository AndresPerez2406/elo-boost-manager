from core.database import agregar_booster, obtener_boosters, eliminar_booster

# 1. Intentamos agregar
print("--- PRUEBA DE INSERT ---")
agregar_booster("Faker")
agregar_booster("Chovy")
agregar_booster("Faker") # Debería dar error de duplicado

# 2. Leemos
print("\n--- LISTA ACTUAL ---")
lista = obtener_boosters()
print(lista) # Debería salir [(1, 'Faker'), (2, 'Chovy')]

# 3. Borramos
print("\n--- PRUEBA BORRAR ---")
eliminar_booster(1) # Borramos a Faker
print(obtener_boosters())

# Ejecuta esto para "despertar" los pedidos viejos
import sqlite3
conn = sqlite3.connect("perezboost.db")
conn.execute("UPDATE pedidos SET estado = 'Activo' WHERE estado IS NULL OR estado = ''")
conn.commit()
conn.close()
print("✅ Pedidos antiguos actualizados a 'Activo'.")