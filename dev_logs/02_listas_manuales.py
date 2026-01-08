print("--- PASO 2: LISTAS Y EDICIÓN ---")

lista_pedidos = []

pedido_1 = { "cliente": "Naut", "liga": "Oro", "precio": 20 }
pedido_2 = { "cliente": "Askariz", "liga": "Platino", "precio": 35 }

lista_pedidos.append(pedido_1)
lista_pedidos.append(pedido_2)

# Editamos un dato
print("Antes:", lista_pedidos[1])
lista_pedidos[1]["liga"] = "Diamante 1"
print("Ahora:", lista_pedidos[1])

# Accedemos a un dato específico
print(f"Precio del primer pedido: {lista_pedidos[0]['precio']}")