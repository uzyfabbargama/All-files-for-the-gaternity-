from ursina import *
import ctypes
import random

# --- Conexión con tu Magia Negra ---
lib = ctypes.CDLL("./libnum.so")

# Definimos 1000 cubos
N = 1000
# Cada cubo tiene X e Y, y cada eje tiene Entero y Decimal (4 QWORDS por cubo)
# Mente de Posiciones: [DecX, IntX, DecY, IntY] * N
mente_pos = (ctypes.c_uint64 * (N * 4))()
# Mente de Velocidades: [DecX, IntX, DecY, IntY] * N
mente_vel = (ctypes.c_uint64 * (N * 4))()

# Inicializamos con valores aleatorios (Simulando carga NMXT)
for i in range(N * 4):
    mente_pos[i] = random.randint(0, 100) # Posiciones locas
    mente_vel[i] = random.randint(1000000, 5000000) # Velocidades pequeñas en el decimal

app = Ursina()

# Creamos los cubos en Ursina (solo visual)
visuales = [Entity(model='cube', scale=0.1, color=color.random_color()) for _ in range(N)]

def update():
    # 1. LLAMADA MAESTRA AL ASM
    # Le pasamos las dos mentes y la cantidad de QWORDS a procesar (N * 4)
    lib._nmxt_update(mente_pos, mente_vel, N * 4)

    # 2. Sincronizamos Ursina con tu motor
    for i in range(N):
        # Extraemos la parte entera de X (índice 1) y de Y (índice 3)
        x_int = mente_pos[i*4 + 1]
        y_int = mente_pos[i*4 + 3]
        
        # Un pequeño rebote simple en Python para no complicar el ASM hoy
        # (Si la posición se sale, invertimos la velocidad en la mente)
        if x_int > 20 or x_int < 0: 
            mente_vel[i*4 + 1] = (2**64 - mente_vel[i*4 + 1]) # Invertir en complemento a 2
            
        visuales[i].x = (x_int % 20) - 10
        visuales[i].y = (y_int % 20) - 5

EditorCamera()
app.run()
