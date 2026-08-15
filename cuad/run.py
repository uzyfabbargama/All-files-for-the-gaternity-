import time

def fastSquare(n):
    # El Peaje Transurgente
    if n > 0 and (n & (n + 1)) == 0:
        bits = n.bit_length()
        x = (n << (bits + 1)) ^ (n << 1)
        return n ^ x
    return n * n

def carrera():
    iteraciones = 10_000_000
    
    # 1. El Pequeño (2**2) - Referencia de control
    start = time.perf_counter()
    for _ in range(iteraciones):
        _ = 2 * 2
    t_control = time.perf_counter() - start
    print(f"[*] 2*2 (Referencia): {t_control:.4f}s")

    # 2. El Camino Lento (17**2) - Aritmética pura
    start = time.perf_counter()
    for _ in range(iteraciones):
        _ = 17 * 17
    t_lento = time.perf_counter() - start
    print(f"[*] 17*17 (Lento):    {t_lento:.4f}s")

    # 3. Tu Truco (31**2) - Pasando por el peaje transurgente
    # Nota: Aquí incluimos el tiempo de la función completa (if + lógica)

carrera()
start = time.perf_counter()
for _ in range(10_000):
    _ = fastSquare(31)
t_truco = time.perf_counter() - start
print(f"[*] 31^2 (Tu truco):  {t_truco:.4f}s")
