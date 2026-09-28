import sys

def float_to_custom56(val: float) -> int:
    """ Convierte un float (0.0 a 1.999...) al formato entero de 56 bits. """
    entero = 1 if val >= 1.0 else 0
    frac = val - entero
    frac_bits = int(frac * (2 ** 55))
    return (entero << 55) | (frac_bits & ((1 << 55) - 1))

def custom56_to_float(val_int: int) -> float:
    """ Convierte el entero de 56 bits de vuelta a float. """
    entero = (val_int >> 55) & 1
    frac_bits = val_int & ((1 << 55) - 1)
    return entero + (frac_bits / (2 ** 55))

def procesar_neurona(val_a: float, val_b: float):
    # 1. Cargar neuronas A y B en formato 56 bits
    r12 = float_to_custom56(val_a)
    r13 = float_to_custom56(val_b)
    r15 = 0  # Estado inicial de r15

    # --- SIMULACIÓN DE RUTINA NASM ---
    # or r15, r12
    r15 = (r15 | r12) & 0xFFFFFFFFFFFFFFFF
    
    # and r15, r13 (Producto lógico / Intersección)
    r15 = (r15 & r13) & 0xFFFFFFFFFFFFFFFF
    
    # add r12, r15
    r12 = (r12 + r15) & 0xFFFFFFFFFFFFFFFF
    
    # add r13, r15
    r13 = (r13 + r15) & 0xFFFFFFFFFFFFFFFF
    
    # add r13, r12
    r13 = (r13 + r12) & 0xFFFFFFFFFFFFFFFF
    
    # add r15, r13
    r15 = (r15 + r13) & 0xFFFFFFFFFFFFFFFF
    
    # shl r15, 1
    r15 = (r15 << 1) & 0xFFFFFFFFFFFFFFFF
    # shr r15, 55 (Aísla el MSB del formato de 56 bits)
    r15 = (r15 >> 55) & 0xFFFFFFFFFFFFFFFF
    #and r15. 1
    r15 = (r15 & 1) & 0xFFFFFFFFFFFFFFFF
    
    r9 = r15 & 0xFF  # El byte de disparo resultante (0 o 1)

    # Reconstruimos el valor numérico acumulado en r13 antes del disparo para ver la escala
    val_resultado = custom56_to_float(r13 & ((1 << 56) - 1))

    return {
        "disparo_r9": r9,
        "acumulado_float_r13": val_resultado,
        "r15_raw_hex": hex(r15)
    }

# --- PRUEBA CON 0.5 y 0.1 ---
#A = float(input("Ingresa el primer  número: "))
#B = float(input("Ingresa el segundo número: "))
A = float(sys.argv[1])
B = float(sys.argv[2])
resultado = procesar_neurona(A, B)

print("--- RESULTADO DE LA PROCESACIÓN ---")
print(f"Neurona A: {A} | Neurona B: {B}")
print(f"Bit de Disparo (r9): {resultado['disparo_r9']}")
print(f"Acumulado resultante en R13 (Float aproximado): {resultado['acumulado_float_r13']:.10f}")
