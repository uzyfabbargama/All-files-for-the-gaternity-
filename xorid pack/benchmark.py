import xip  # ¡Tu librería!
import json
import time

# 1. PREPARACIÓN DE DATOS (10,000 variables)
datos_prueba = {f"variable_numero_{i}": i for i in range(10000)}

# Guardamos ambos formatos
xip.dump(datos_prueba, "test.xip")
with open("test.json", "w") as f:
    json.dump(datos_prueba, f)

print("--- INICIANDO BENCHMARK (10,000 REGISTROS) ---")

# 2. TEST JSON
inicio_json = time.perf_counter()
with open("test.json", "r") as f:
    res_json = json.load(f)
fin_json = time.perf_counter()
tiempo_json = (fin_json - inicio_json) * 1000

# 3. TEST XIP (Tu estándar)
inicio_xip = time.perf_counter()
res_xip = xip.load("test.xip")
fin_xip = time.perf_counter()
tiempo_xip = (fin_xip - inicio_xip) * 1000

# 4. RESULTADOS
print(f"Tiempo JSON: {tiempo_json:.4f} ms")
print(f"Tiempo XIP:  {tiempo_xip:.4f} ms")
print(f"\nDiferencia: XIP es {tiempo_json/tiempo_xip:.2f} veces más rápido en lógica de lexeo.")
