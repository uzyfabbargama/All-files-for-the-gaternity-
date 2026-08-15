import time

def mostrar_bits(nombre, valor):
    print(f"[*] {nombre:<18}: {valor:<10} | Bin: {bin(valor)[2:]:>12}")

def test_transurgencia(n, bits_shift, correccion_u):
    print(f"\n--- ANALIZANDO EL {n} ---")
    n_real_cuadrado = n * n
    
    # 1. Tu Geometría Visual (Duplicar y XOR)
    # x = (n << (bits_totales + 1)) ^ (n << 1)
    x = (n << bits_shift) ^ (n << 1)
    r_sucio = n ^ x
    
    # 2. Tu "Puente de Uziel" (La correccion basada en el 100/4)
    # Para el 13, la formula que descubrimos: r - (n * ((n << 1) - 4))
    r_final = r_sucio - correccion_u
    
    mostrar_bits("Número n", n)
    mostrar_bits("Resultado Sucio", r_sucio)
    mostrar_bits("Corrección Aplicada", correccion_u)
    mostrar_bits("Resultado Final", r_final)
    mostrar_bits("Objetivo Real", n_real_cuadrado)
    
    if r_final == n_real_cuadrado:
        print("¡EUREKA! La transurgencia es perfecta.")
    else:
        print(f"[-] Error residual: {r_final - n_real_cuadrado}")

# --- EJECUCIÓN ---

# Test del 13 (bits_shift = 5 porque 13 tiene 4 bits)
# Tu formula: n * ((n << 1) - 4) = 13 * (26 - 4) = 13 * 22 = 286
n_13 = 13
corr_13 = n_13 * ((n_13 << 1) - 4)
test_transurgencia(n_13, 5, corr_13)

# Test del 5 (bits_shift = 4 porque 5 tiene 3 bits)
# ¿Seguirá el patrón del "100"? 
# n=5 (101), k=1. Intentemos: 5 * ((5 << 1) - 4) = 5 * (10 - 4) = 30
n_5 = 5
corr_5 = n_5 * ((n_5 << 1) - 4) 
test_transurgencia(n_5, 4, corr_5)
