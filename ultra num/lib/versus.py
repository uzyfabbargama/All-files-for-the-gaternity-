import numpy as np
import time
import ctypes

# --- Configuración NMXT ---
# Asumiendo que ya tienes libnum.so compilada
lib = ctypes.CDLL("./libnum.so")
mente = (ctypes.c_int64 * 2000000)() # Espacio para 1M de números (e, d)

def test_nmxt(texto_nmxt):
    start = time.perf_counter()
    lib._nmxt_parser(ctypes.c_char_p(texto_nmxt), mente)
    end = time.perf_counter()
    return end - start

def test_numpy(filename):
    start = time.perf_counter()
    data = np.loadtxt(filename, delimiter=',')
    end = time.perf_counter()
    return end - start

# --- Generar datos de prueba ---
print("Generando 1,000,000 de pesos...")
pesos = np.random.rand(1000000)

# Guardar para NumPy
np.savetxt("pesos.csv", pesos, delimiter=",")

# Guardar para NMXT (Formato legible que propusimos)
with open("pesos.nmxt", "w") as f:
    for p in pesos:
        val = int(p * (2**32))
        f.write(f"int: 32 frac: 32 sep {val} ,,")

# --- CORRER EL DUELO ---
with open("pesos.nmxt", "rb") as f:
    raw_nmxt = f.read()

t_nmxt = test_nmxt(raw_nmxt)
t_np = test_numpy("pesos.csv")

print(f"\n--- RESULTADOS ---")
print(f"NumPy (loadtxt): {t_np:.4f} segundos")
print(f"Tu Motor NMXT:  {t_nmxt:.4f} segundos")
print(f"¡Tu motor es {t_np/t_nmxt:.1f} veces más rápido!")
