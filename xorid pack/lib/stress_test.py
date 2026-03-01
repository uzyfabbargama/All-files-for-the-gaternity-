from xip import XIP
import time
import random

# 1. Inicializar la "Mente"
motor = XIP(buffer_size_mb=2) # Subimos a 2MB por si acaso

# 2. Generar datos de 10.000 entidades (X, Y, Z)
num_entidades = 10000
print(f"--- GENERANDO {num_entidades * 3} COORDENADAS ---")

datos_lista = []
for i in range(num_entidades):
    # Creamos la trama: eID_x::VAL,,eID_y::VAL,,eID_z::VAL,,
    datos_lista.append(f"e{i}_x::{random.randint(0, 1000)},,")
    datos_lista.append(f"e{i}_y::{random.randint(0, 1000)},,")
    datos_lista.append(f"e{i}_z::{random.randint(0, 1000)},,")

raw_data = "".join(datos_lista)

# 3. EL GRAN TEST DE VELOCIDAD
print("Inyectando enjambre en la CPU...")
start = time.time()
motor.inyectar(raw_data)
end = time.time()

t_total = end - start

# 4. Verificación de un robot aleatorio
test_id = random.randint(0, num_entidades - 1)
print(f"\n--- VERIFICACIÓN ENTIDAD {test_id} ---")
print(f"Posición X: {motor[f'e{test_id}_x']}")
print(f"Posición Y: {motor[f'e{test_id}_y']}")
print(f"Posición Z: {motor[f'e{test_id}_z']}")

print(f"\nVelocidad: {t_total:.6f} segundos.")
print(f"Rendimiento: {int((num_entidades * 3) / t_total)} coordenadas por segundo.")
