from ursina import *
import numpy as np 

# --- Configuración de Numerium ---
N_CHUNK_SIZE = 16  # N para el chunk NxN (ej. 16x16)
BASE_NUMERIUM = N_CHUNK_SIZE**2 + 1 # 16^2 + 1 = 257
MAX_HEIGHT = 32 # Altura máxima para la visualización del prototipo (ajustable)

# Una única semilla global que define el mundo.
# ¡Cambia este número para generar mundos diferentes y observa los patrones!
GLOBAL_SEED = 11 # Ejemplos: 11, 23, 45, etc.

# Diccionario para almacenar las entidades (bloques) por posición.
# Usaremos un conjunto para verificar rápidamente si una posición está ocupada.
terrain_blocks = set() 

# --- Funciones de Numerium ---

def get_digit_in_base(number, base, position):
    """
    Obtiene el 'dígito' en una posición específica (0 para unidades, 1 para 'decenas', etc.)
    cuando el número se expresa en la BASE_NUMERIUM.
    Este dígito puede ir de 0 a (base - 1).
    """
    if number < 0:
        number = abs(number)
    
    power = base**position
    return (number // power) % base

def get_block_color(height):
    """
    Asigna un color al bloque basado en su altura (Y).
    """
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
    """
    Genera un chunk de terreno Numerium usando una única semilla global
    y tu lógica de multiplicación de la semilla por posición.
    """
    print(f"Generando chunk Numerium con Semilla Global={global_seed}, Base={BASE_NUMERIUM}...")

    # Array 3D (X, Y, Z) para rastrear las posiciones ocupadas LOCALES del chunk.
    occupied_positions_local = np.full((N_CHUNK_SIZE, MAX_HEIGHT, N_CHUNK_SIZE), False, dtype=bool)

    # Offset global para el chunk (si generamos múltiples chunks)
    chunk_offset_x = start_x * N_CHUNK_SIZE
    chunk_offset_z = start_z * N_CHUNK_SIZE

    # --- Iterar sobre el plano X, Z para generar bloques ---
    for z_local in range(N_CHUNK_SIZE):
        for x_local in range(N_CHUNK_SIZE):
            x_global = chunk_offset_x + x_local
            z_global = chunk_offset_z + z_local

            # --- Calcular la Semilla Transformada para esta posición (X, Z) ---
            semilla_transformada = global_seed
            
            semilla_transformada *= (x_global + 1) 
            
            if z_global > 0:
                semilla_transformada *= (18 * z_global) 
            else:
                semilla_transformada *= 1 

            if semilla_transformada == 0:
                semilla_transformada = global_seed if global_seed != 0 else 1 

            # --- Cálculo de Altura (Y) con los 'dígitos' de la Semilla Transformada ---
            initial_y_scaled = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 0) // (BASE_NUMERIUM // MAX_HEIGHT)
            
            modifier_y_digit = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 1)
            
            current_y = initial_y_scaled + (modifier_y_digit % 3) 

            current_y = max(0, min(current_y, MAX_HEIGHT - 1))

            # --- Aplicación de la Regla 2: Conflicto de Posición ---
            while True:
                if current_y >= MAX_HEIGHT:
                    break 

                if not occupied_positions_local[x_local, int(current_y), z_local]:
                    break
                
                current_y += 1
            
            # --- Creación del Bloque (Entity) ---
            if current_y < MAX_HEIGHT:
                occupied_positions_local[x_local, int(current_y), z_local] = True
                
                block_color = get_block_color(current_y)

                block = Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, current_y, z_global),
                    scale=1,
                    # No especificamos textura para evitar posibles problemas con 'white_cube'
                    # y que el color sea directamente visible.
                    parent=scene,
                    # Añadir un componente de shader para que reciba iluminación
                    # (Esto es opcional si no hay luces complejas, pero ayuda a que se vea 3D)
                    shader=unlit_shader # o lit_shader si hay luces
                )