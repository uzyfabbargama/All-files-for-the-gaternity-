from ursina import *
from ursina.shaders import lit_shader # ¡Vamos a usar lit_shader para ver las sombras!
import numpy as np 

# --- Configuración de Numerium ---
N_CHUNK_SIZE = 16  # N para el chunk NxN (ej. 16x16)
BASE_NUMERIUM = N_CHUNK_SIZE**2 + 1 # 16^2 + 1 = 257
MAX_HEIGHT = 32 # Altura máxima para la visualización del prototipo (ajustable)

# Una única semilla global que define el mundo.
GLOBAL_SEED = 11 

# Diccionario para almacenar las entidades (bloques) por posición.
terrain_blocks = set() 

# --- Funciones de Numerium ---

def get_digit_in_base(number, base, position):
    if number < 0:
        number = abs(number)
    
    power = base**position
    return (number // power) % base

def get_block_color(height):
    if height < 2: 
        return color.gray # Roca
    elif height < 5: 
        return color.rgb(139, 69, 19) # Tierra (Marrón)
    elif height < 8: 
        return color.green # Pasto
    elif height < 12:
        return color.rgb(100, 100, 100) # Montaña rocosa
    else: 
        return color.white # Nieve en las cimas

def generate_numerium_chunk(global_seed, start_x=0, start_z=0):
    print(f"Generando chunk Numerium con Semilla Global={global_seed}, Base={BASE_NUMERIUM}...")

    occupied_positions_local = np.full((N_CHUNK_SIZE, MAX_HEIGHT, N_CHUNK_SIZE), False, dtype=bool)

    chunk_offset_x = start_x * N_CHUNK_SIZE
    chunk_offset_z = start_z * N_ quizásN_CHUNK_SIZE

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

                # Usamos 'lit_shader' para que la luz afecte los cubos y veamos las sombras
                block = Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, current_y, z_global),
                    scale=1,
                    parent=scene,
                    shader=lit_shader # <--- CAMBIO IMPORTANTE AQUÍ
                )

# --- Configuración de Ursina ---
app = Ursina()

# --- CAMBIO IMPORTADO: Configuración de la Ventana y Fondo ---
# Aseguramos un color de fondo diferente para que contraste
window.color = color.rgb(70, 100, 120) # Un azul cielo oscuro para mejor contraste

# --- Iluminación: Crucial para ver objetos con lit_shader ---
# Una luz direccional (como el sol)
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1)) # Viene de arriba a la derecha

# Una luz ambiental para que las caras en sombra no sean completamente negras
AmbientLight(color=color.rgba(70, 70, 70, 255)) 

# --- Configuración de Cámara: Más alta y con un ángulo que garantice visibilidad ---
EditorCamera() 
camera.orthographic = True 
# Posición: más alta y un poco más retirada del chunk para verlo completo
camera.position = (N_CHUNK_SIZE / 2, MAX_HEIGHT * 3, -N_CHUNK_SIZE * 1.5) # Más altura y más atrás en Z
camera.rotation_x = -45 # Mirando hacia abajo

# FOV: Es importante para la vista ortográfica; asegúrate de que el chunk quepa
# Puedes ajustarlo; un valor más grande mostrará más del mundo
camera.fov = N_CHUNK_SIZE * 2 # Aumentado el FOV un poco más

# --- Generar el Mundo Numerium ---
generate_numerium_chunk(GLOBAL_SEED, start_x=0, start_z=0)

# --- Bucle principal de Ursina ---
app.run()