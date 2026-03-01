from ursina import *
from ursina.shaders import unlit_shader # ¡IMPORTAR ESTO!
import numpy as np 

# --- Configuración de Numerium ---
N_CHUNK_SIZE = 16
BASE_NUMERIUM = N_CHUNK_SIZE**2 + 1
MAX_HEIGHT = 32

GLOBAL_SEED = 11

terrain_blocks = set()

# --- Funciones de Numerium ---

def get_digit_in_base(number, base, position):
    if number < 0:
        number = abs(number)
    
    power = base**position
    return (number // power) % base

def get_block_color(height):
    if height < 2: 
        return color.gray
    elif height < 5: 
        return color.rgb(139, 69, 19)
    elif height < 8: 
        return color.green
    elif height < 12:
        return color.rgb(100, 100, 100)
    else: 
        return color.white

def generate_numerium_chunk(global_seed, start_x=0, start_z=0):
    print(f"Generando chunk Numerium con Semilla Global={global_seed}, Base={BASE_NUMERIUM}...")

    occupied_positions_local = np.full((N_CHUNK_SIZE, MAX_HEIGHT, N_CHUNK_SIZE), False, dtype=bool)

    chunk_offset_x = start_x * N_CHUNK_SIZE
    chunk_offset_z = start_z * N_CHUNK_SIZE

    for z_local in range(N_CHUNK_SIZE):
        for x_local in range(N_CHUNK_SIZE):
            x_global = chunk_offset_x + x_local
            z_global = chunk_offset_z + z_local

            semilla_transformada = global_seed
            
            semilla_transformada *= (x_global + 1)
            
            if z_global > 0:
                semilla_transformada *= (18 * z_global)
            else:
                semilla_transformada *= 1

            if semilla_transformada == 0:
                semilla_transformada = global_seed if global_seed != 0 else 1

            initial_y_scaled = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 0) // (BASE_NUMERIUM // MAX_HEIGHT)
            
            modifier_y_digit = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 1)
            
            current_y = initial_y_scaled + (modifier_y_digit % 3)

            current_y = max(0, min(current_y, MAX_HEIGHT - 1))

            while True:
                if current_y >= MAX_HEIGHT:
                    break 

                if not occupied_positions_local[x_local, int(current_y), z_local]:
                    break
                
                current_y += 1
            
            if current_y < MAX_HEIGHT:
                occupied_positions_local[x_local, int(current_y), z_local] = True
                
                block_color = get_block_color(current_y)

                block = Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, current_y, z_global),
                    scale=1,
                    parent=scene,
                    shader=unlit_shader # Usamos unlit_shader aquí
                )

# --- Configuración de Ursina ---
app = Ursina()

# --- Iluminación (aunque con unlit_shader no es estrictamente necesaria para ver colores, ayuda a dar profundidad) ---
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))
# AmbientLight(color=color.rgba(70, 70, 70, 255)) 

# --- Configuración de Cámara ---
EditorCamera() 
camera.orthographic = True 
camera.position = (N_CHUNK_SIZE / 2, MAX_HEIGHT * 2.5, -N_CHUNK_SIZE * 0.75)
camera.rotation_x = -45 
camera.fov = N_CHUNK_SIZE * 1.5 

# --- Generar el Mundo Numerium ---
generate_numerium_chunk(GLOBAL_SEED, start_x=0, start_z=0)

# --- Bucle principal de Ursina ---
app.run()