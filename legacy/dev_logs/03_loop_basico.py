print("--- PASO 3: LOOP INTERACTIVO ---")

lista_pedidos = []

while True:
    print("\n--- NUEVA ORDEN ---")
    nombre = input("Cliente: ")
    precio = int(input("Precio ($): ")) 
    
    nuevo_pedido = { "cliente": nombre, "precio": precio }
    lista_pedidos.append(nuevo_pedido)
    
    if input("¿Otra? (si/no): ") == "no":
        break

# Suma total simple
total = 0
for p in lista_pedidos:
    total += p["precio"]

print(f"Total caja: ${total}")