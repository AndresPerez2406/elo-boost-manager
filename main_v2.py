import os

# --- ZONA DE FUNCIONES (Tus Herramientas) ---

def pedir_si_no(mensaje):
    """Pregunta s/n y solo devuelve True (si) o False (no)"""
    while True:
        respuesta = input(mensaje).lower() # Convertimos a minuscula (S -> s)
        if respuesta == "s":
            return True
        elif respuesta == "n":
            return False
        else:
            print("❌ Opción no válida. Escribe 's' o 'n'.")

def pedir_numero(mensaje):
    """Pide un numero y no te deja avanzar hasta que sea valido"""
    while True:
        try:
            # Intentamos convertir lo que escriba a numero
            dato = int(input(mensaje))
            return dato # Si funciona, devolvemos el numero y rompemos el loop
        except ValueError:
            # Si falla (escribio letras), caemos aqui
            print("❌ ¡Error! Por favor ingresa solo números (Ej: 20).")

def limpiar_pantalla():
    """Limpia la consola para que se vea pro"""
    os.system('cls' if os.name == 'nt' else 'clear')

def calcular_ganancia(cobro, pago_booster):
    """Recibe dos numeros y devuelve la resta"""
    return cobro - pago_booster

def mostrar_reporte(lista_pedidos):
    """Imprime el reporte final bonito"""
    print("\n" + "="*40)
    print("📊 REPORTE FINAL DE ELO-BOOST 📊")
    print("="*40)
    
    total_caja = 0
    
    for p in lista_pedidos:
        print(f"[{p['estado']}] {p['cuenta']} | Booster: {p['booster']} | Profit: ${p['ganancia']}")
        if p['estado'] == "Terminado":
            
            total_caja += p['ganancia']
            
    print("-" * 40)
    print(f"💰 GANANCIA TOTAL EN CAJA: ${total_caja}")
    print("=" * 40)

# --- ZONA PRINCIPAL (Donde ocurre la magia) ---

pedidos = []

while True:
    limpiar_pantalla()
    print("--- NUEVO PEDIDO ---")
    
    # 1. Pedir Datos
    cuenta = input("Nombre de Cuenta: ")
    booster = input("Nombre del Booster: ")
    precio_cliente = pedir_numero("Cobro al Cliente ($): ")
    pago_booster = pedir_numero("Pago al Booster ($): ")
    
    # 2. Usar nuestra funcion magica
    profit = calcular_ganancia(precio_cliente, pago_booster)
    
    # 3. Guardar
    estado = pedir_si_no("¿Terminado? (s/n): ")
    estado_final = "Terminado" if estado == "s" else "Pendiente"
    
    nuevo_ticket = {
        "cuenta": cuenta,
        "booster": booster,
        "ganancia": profit,
        "estado": estado_final
    }
    
    pedidos.append(nuevo_ticket)
    print(f"✅ Pedido guardado. Ganancia calculada: ${profit}")
    
    # 4. Continuar?
    if pedir_si_no("\n¿Agregar otro? (Enter=Si, 'n'=No): ") == False:
        break

# Al final, llamamos a la funcion de reporte
mostrar_reporte(pedidos)