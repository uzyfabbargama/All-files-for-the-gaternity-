import time



# --- 1. REFERENCIA (2*2) ---
start = time.perf_counter()
for _ in range(10_000_000):
    _ = 2 * 2
t_ref = time.perf_counter() - start

# --- 2. CAMINO LENTO (30*30) ---
start = time.perf_counter()
for _ in range(10_000_000):
    _ = 30 * 30
t_lento = time.perf_counter() - start

# --- 3. TU TRUCO COMPENSADO (30^2) ---
# n = 30 (11110)
# bits = 5
start = time.perf_counter()
n = ((2**1024) - 1)*2
for _ in range(10_000_000):
    # Duplicamos, XOR y restamos el doble (Compensación Eureka)
    # k = 1024 bits
    _ = (n ^ ((n << 1025) ^ (n << 1))) - (n << 1)
t_eureka = time.perf_counter() - start

print(f"[*] 2*2 (Referencia):     {t_ref:.4f}s")
print(f"[*] 30*30 (Lento):        {t_lento:.4f}s")
print(f"[*] 30^2 (Tu Transurgencia): {t_eureka:.4f}s")
print(f"\n[!] Diferencia: El truco es {t_lento/t_eureka:.2f} veces más rápido.")
