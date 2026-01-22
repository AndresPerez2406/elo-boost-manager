print("--- MANAGER DE ELO-BOOST V2.3 (Lógica Real) ---")

lista_pedidos = []

while True:
    print("\n--- NUEVA ORDEN ---")
    
    cuenta = input("Cuenta (Usuario): ")
    booster = input("Booster Asignado: ")
    
    # 1. ESTADO
    print("Estado: 1. Subiendo | 2. Terminada")
    if input("Elige (1 o 2): ") == "1":
        estado_real = "🟡 Subiendo"
    else:
        estado_real = "🟢 Terminada"

    # 2. FINANZAS
    cobro = int(input("Cobro ($): ")) 
    pago = int(input("Pago al Booster ($): "))
    mi_ganancia = cobro - pago
    
    nuevo_pedido = {
        "cuenta": cuenta,
        "booster": booster,
        "ingreso": cobro,
        "gasto": pago,
        "estado": estado_real,
        "profit": mi_ganancia
    }
    
    lista_pedidos.append(nuevo_pedido)
    
    if input("¿Otra? (si/no): ") == "no":
        break

# --- REPORTE INTELIGENTE ---
print("\n" + "="*40)
print(" ESTADO DE CUENTAS ")
print("="*40)

dinero_en_mano = 0   # Solo cuentas terminadas
dinero_pendiente = 0 # Cuentas subiendo

for pedido in lista_pedidos:
    
    # IMPRIMIMOS LA FILA SIEMPRE
    print(f"[{pedido['estado']}] {pedido['cuenta']} | Booster: {pedido['booster']} | Pago Recibido: ${pedido['ingreso']} || Pago Booster: ${pedido['gasto']} | Profit: ${pedido['profit']}")
    # LÓGICA DE SUMA CONDICIONAL
    if pedido['estado'] == "🟢 Terminada":
        dinero_en_mano += pedido['profit']  # ¡Caja real!
    else:
        dinero_pendiente += pedido['profit'] # Dinero futuro

print("-" * 40)
print(f" DINERO YA GANADO (Real):   ${dinero_en_mano}")
print(f" DINERO POR ENTRAR (Futuro): ${dinero_pendiente}")
print("=" * 40)