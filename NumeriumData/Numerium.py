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
terrain_blocks = set() # Usar un set para `(x,y,z)` para verificación rápida `in`

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
    Asigna un color al bloque basado en su altura (Y) para simular materiales.
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

def generate_numerium_chunk(global_seed,  start_x = 0, start_z = 0):
   
    """
    Genera un chunk de terreno Numerium usando una única semilla global
    y tu lógica de multiplicación de la semilla por posición.
    """
    print(f"Generando chunk Numerium con Semilla Global={global_seed}, Base={BASE_NUMERIUM}...")

    # Array 3D (X, Y, Z) para rastrear las posiciones ocupadas LOCALES del chunk.
    # Usamos np.full con dtype=bool para eficiencia
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
            # La lógica de multiplicación es crucial aquí
            semilla_transformada = global_seed
            
            # Aplicar la multiplicación por X+1
            semilla_transformada *= (x_global + 1)
            
            # Aplicar la multiplicación por Z (usando tu factor de 18)
            # Aseguramos que si z_global es 0, no multipliquemos por 0, sino por 1
            if z_global > 0:
                semilla_transformada *= (18 * z_global) # Tu factor de 18 para el salto en Z

            # Asegurarnos de que el número no sea 0 si la semilla es 0, o por alguna multiplicación
            if semilla_transformada == 0:
                semilla_transformada = global_seed # O algún valor por defecto si 0 es un problema

            # --- Cálculo de Altura (Y) con los 'dígitos' de la Semilla Transformada ---
            # Usamos el 'dígito de la unidad' (posición 0) de la semilla_transformada en BASE_NUMERIUM
            # para la altura principal.
            # El dígito puede ir de 0 a 256. Lo escalamos para que quepa en MAX_HEIGHT.
            # Por ejemplo, dividirlo por (BASE_NUMERIUM // MAX_HEIGHT)
            
            # Una forma simple de escalar el dígito para que dé alturas dentro de MAX_HEIGHT
            # Por ejemplo, si el dígito es 0..256, y MAX_HEIGHT es 32, dividimos por 8.
            initial_y_scaled = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 0) // (BASE_NUMERIUM // MAX_HEIGHT)
            
            # Podemos usar el 'dígito de la decena' (posición 1) para añadir variación o detalle.
            modifier_y_digit = get_digit_in_base(semilla_transformada, BASE_NUMERIUM, 1)
            
            # Combinar la altura inicial con un modificador
            current_y = initial_y_scaled + (modifier_y_digit % 3) # Pequeño ajuste para más variedad

            # Asegurar que la altura no sea negativa y esté dentro de MAX_HEIGHT
            current_y = max(0, min(current_y, MAX_HEIGHT - 1))

            # --- Aplicación de la Regla 2: Conflicto de Posición ---
            # Si un bloque intenta ocupar el lugar de otro, salta de capa (aumenta Y)
            original_y = current_y # Guardar la altura calculada antes de la resolución de conflicto
            
            while True:
                # Si la altura excede el límite, detenemos la creación del bloque para esta posición
                if current_y >= MAX_HEIGHT:
                    break 

                # Comprobar si la posición (x_local, current_y, z_local) ya está ocupada en el array local
                if not occupied_positions_local[x_local, int(current_y), z_local]:
                    # Posición libre, salimos del bucle para colocar el bloque
                    break
                
                # Si está ocupada, incrementamos Y y volvemos a intentar
                current_y += 1
            
            # --- Creación del Bloque (Entity) ---
            # Solo si encontramos una posición válida dentro de MAX_HEIGHT
            if current_y < MAX_HEIGHT:
                # Marcar la posición LOCAL como ocupada
                occupied_positions_local[x_local, int(current_y), z_local] = True
                
                # Asignar color basado en la altura final
                block_color = get_block_color(current_y)

                # Crear la entidad en Ursina con las coordenadas GLOBALES
                block = Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, current_y, z_global),
                    scale=1, # Escala 1 para bloques de tamaño estándar
                    texture='white_cube', # Textura simple para visualización
                    parent=scene
                )
                # Opcional: Si quieres un conjunto para todos los bloques globales (para otros fines)
                # terrain_blocks.add((x_global, current_y, z_global))


# --- Configuración de Ursina ---
app = Ursina()

# Configurar la cámara para una vista aérea
EditorCamera() 
camera.orthographic = True 
# Ajustar la posición de la cámara para centrarse en el chunk y ver desde arriba
camera.position = (N_CHUNK_SIZE / 2 + start_x * N_CHUNK_SIZE, MAX_HEIGHT * 2, N_CHUNK_SIZE / 2 + start_z * N_CHUNK_SIZE) 
camera.rotation_x = -60 
camera.fov = N_CHUNK_SIZE * 1.5 

# --- Generar el Mundo Numerium ---
# Llamamos a la función con la semilla global
generate_numerium_chunk(GLOBAL_SEED, start_x=0, start_z=0)

# Opcional: Generar algunos chunks adyacentes.
# Observa cómo los patrones continúan o se transforman.
# generate_numerium_chunk(GLOBAL_SEED, start_x=1, start_z=0) # Chunk a la derecha
# generate_numerium_chunk(GLOBAL_SEED, start_x=0, start_z=1) # Chunk hacia adelante
# generate_numerium_chunk(GLOBAL_SEED, start_x=1, start_z=1) # Chunk diagonal

# --- Bucle principal de Ursina ---
app.run()