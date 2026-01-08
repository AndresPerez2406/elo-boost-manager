print("--- PASO 1: DICCIONARIOS ---")

# Creamos una sola ficha técnica
pedido_actual = {
    "cliente": "JuanPerez",
    "cuenta_lol": "YasuoMain123",
    "booster_asignado": "Naut",
    "liga_entrega": "Diamante 4",
    "dinero_recibido": 25,
    "pago_booster": 15,
    "estado": "Subiendo"
}

# Calculamos ganancia simple
ingreso_total = pedido_actual["dinero_recibido"]
gasto_booster = pedido_actual["pago_booster"]
mi_ganancia = ingreso_total - gasto_booster

print(f"Cuenta: {pedido_actual['cuenta_lol']}")
print(f"Ganancia Neta: ${mi_ganancia}")