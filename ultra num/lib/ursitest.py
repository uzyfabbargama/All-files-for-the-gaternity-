from ursina import *
import ctypes
from numext import NumExt # Tu clase envoltorio

app = Ursina()

# 1. Cargamos el Motor y procesamos los pesos
# Supongamos que generamos 20,000 números (10k para X, 10k para Y)
motor = NumExt(max_numeros=20000)
with open("pesos.nmxt", "rb") as f:
    datos_crudos = f.read()

print("Inyectando datos en el motor ASM...")
motor.procesar_archivo(datos_crudos)

# 2. Creamos la representación visual
cubos = []
for i in range(1000):
    # Extraemos posición X y Y desde nuestra "Mente" de 128 bits
    # Convertimos el punto fijo a float para Ursina
    entero_x, frac_x = motor.obtener_numero(i)
    entero_y, frac_y = motor.obtener_numero(i + 10000)
    
    # Reconstrucción del valor (Normalizado para la pantalla)
    pos_x = (entero_x + (frac_x / (2**32))) % 20 - 10
    pos_y = (entero_y + (frac_y / (2**32))) % 20 - 10
    
    c = Entity(model='cube', color=color.random_color(), scale=0.1)
    c.position = (pos_x, pos_y, 0)
    cubos.append(c)

EditorCamera() # Para que podamos navegar la nube de datos
app.run()
