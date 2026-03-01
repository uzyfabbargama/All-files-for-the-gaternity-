from xip import XIP
import time

# 1. Preparación (Fuera del reloj)
motor = XIP(buffer_size_mb=1)
raw_data = "vida::100,,mana::500,,fuerza::9999,,"
# 2. EL MOMENTO DE LA VERDAD
start = time.time()
motor.inyectar(raw_data)
end = time.time()
# ¡Ahora usas el nombre, no el número!
print(f"Vida: {motor['vida']}")   # Python calcula 1402 internamente
print(f"Mana: {motor['mana']}")   # Python calcula 1186 internamente
print(f"Fuerza: {motor['fuerza']}")
print(f"Carga: {end - start:.8f} seg")
