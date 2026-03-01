from xip import XIP
import time
# Iniciar el motor
start = time.time()
motor = XIP(buffer_size_mb=1)
t_xip = time.time() - start
# Inyectar datos masivos
raw_data = "vida::100,,mana::500,,fuerza::9999,,"
motor.inyectar(raw_data)
motor.inyectar(raw_data)

# Mira los primeros 100 slots de la mente para ver dónde inyectó realmente
for i, val in enumerate(motor.mente[:10000]):
    if val > 0:
        print(f"¡Encontré algo! ID: {i} | Valor: {val}")
# Acceder como un jefe
print(f"Vida: {motor[5818]}") # El ID que calculamos antes
print(f"Ha tardado: {t_xip:.5f}seg") 
