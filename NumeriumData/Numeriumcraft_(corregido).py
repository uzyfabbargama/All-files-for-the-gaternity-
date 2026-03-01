import sys
import math
import random
from ursina import Ursina, Entity, color, Button, scene, camera, application, destroy, mouse # <-- destroy y mouse importados explícitamente
from ursina.prefabs.first_person_controller import FirstPersonController

# --- Lógica de Numerium ---
# Función de mapeo para las coordenadas (x, z) dentro de una cuadrícula
# Replicamos el comportamiento de "pilar" e "inclinación" discutido.
# Para el mapeo de coordenadas, asumimos un "modulo" de 100 para la semilla
# como se hizo en los ejemplos de las duplas 50, 51, 55.
def map_value_to_coords(val, grid_x, grid_z):
    # Aseguramos que el valor esté dentro de un rango manejable para el mapeo
    val_mod_mapeo = val % 100 
    
    mapped_x, mapped_z = 0, 0

    # Casos específicos basados en los ejemplos de semillas 50, 51, 55
    # Esto simula el comportamiento de "árboles" o "pilares"
    if val_mod_mapeo in [50, 51, 0, 2, 4, 6, 8, 53, 55, 57, 59]: # 0 para cuando 100, 200, etc.
        mapped_x = 2
        mapped_z = 2
    elif val_mod_mapeo == 10:
        mapped_x = 1
        mapped_z = 1
    else:
        # Mapeo por defecto: usamos la decena para X y la unidad para Z
        # Ajustamos para que siempre estén dentro de la cuadrícula (0 a grid_x/grid_z - 1)
        tens_digit = math.floor(val_mod_mapeo / 10)
        units_digit = val_mod_mapeo % 10
        mapped_x = tens_digit % grid_x
        mapped_z = units_digit % grid_z

    return mapped_x, mapped_z

# Función para generar un chunk de mundo Numerium
# Genera un bloque 3D de voxeles para un chunk específico
def generate_numerium_chunk(seed, chunk_x, chunk_z, chunk_size_x, chunk_size_z, chunk_max_y):
    # Diccionario para almacenar las alturas acumuladas en este chunk
    # Formato: (x_local, z_local) -> altura_y
    chunk_heights = {}
    
    # El valor inicial para la secuencia de Numerium para este chunk
    # Usamos una combinación de la semilla global y las coordenadas del chunk para que sea único
    # Esto es vital para la variación de chunks
    current_sequence_value = seed + (chunk_x * 10000000) + (chunk_z * 10000) # Números más grandes para mayor dispersión
    
    # Lista para almacenar los voxeles finales del chunk para renderizado
    voxels_to_render = []

    # Número de iteraciones para "poblar" el chunk. Esto es clave para la altura y densidad.
    # Un número mayor = más bloques, más altura, más densidad en el chunk.
    # Ajustamos el número de iteraciones para que sea proporcional al tamaño del chunk
    num_filling_iterations = chunk_size_x * chunk_size_z * 10 # Multiplicado por 10 para asegurar varias colisiones

    for _ in range(num_filling_iterations):
        # Mapeamos el valor actual a coordenadas locales dentro del chunk (0 a chunk_size - 1)
        # Usamos 3 como el tamaño de grid para el mapeo base, ya que es lo que hemos estado usando en ejemplos
        x_local_mapped, z_local_mapped = map_value_to_coords(current_sequence_value, 3, 3) 
        
        # Ajustamos las coordenadas mapeadas para que se distribuyan en el tamaño real del chunk
        # Por ejemplo, si map_value_to_coords da (0,0) (1,1) (2,2) etc.
        # Redistribuimos esto sobre el chunk_size real
        x_in_chunk = x_local_mapped % chunk_size_x
        z_in_chunk = z_local_mapped % chunk_size_z

        # Obtenemos la altura actual para esta posición local
        current_y = chunk_heights.get((x_in_chunk, z_in_chunk), 0)

        # Incrementamos la altura para la próxima vez que esta posición sea golpeada
        # Limitamos la altura máxima del chunk para evitar pilares infinitos en un solo spot
        chunk_heights[(x_in_chunk, z_in_chunk)] = min(current_y + 1, chunk_max_y - 1) 

        # Avanzamos la secuencia para la siguiente iteración
        current_sequence_value += seed # Usamos la misma semilla para avanzar la secuencia global

    # Ahora, construimos los voxeles para renderizar basados en las alturas finales
    for x in range(chunk_size_x):
        for z in range(chunk_size_z):
            height = chunk_heights.get((x, z), 0)
            # Para cada nivel hasta la altura generada, añade un bloque
            for y in range(height + 1): # +1 para que un height de 0 tenga un bloque base
                # Coordenadas globales del bloque
                global_x = chunk_x * chunk_size_x + x
                global_y = y # La altura es global
                global_z = chunk_z * chunk_size_z + z
                
                # Asignamos un color simple basado en la altura para diferenciar
                # Esto es solo visual, no representa la "química" de Randomixer todavía
                if global_y < chunk_max_y * 0.3:
                    block_color = color.rgb(80, 40, 20) # Tierra oscura
                elif global_y < chunk_max_y * 0.6:
                    block_color = color.green # Hierba
                else:
                    block_color = color.white # Nieve/Piedra
                
                voxels_to_render.append({'pos': (global_x, global_y, global_z), 'color': block_color})
    return voxels_to_render

# --- Configuración del Juego con Ursina ---
app = Ursina()

# Parámetros del mundo
GLOBAL_SEED = 12345 # Semilla global para el mundo Numerium (puedes cambiarla!)
CHUNK_SIZE = 16    # Tamaño de cada chunk (ej. 16x16 bloques)
RENDER_DISTANCE = 3 # Cuántos chunks alrededor del jugador deben estar cargados (3 = 7x7 chunks en total)
MAX_Y_HEIGHT = 32 # Altura máxima posible para el terreno en un chunk

# Diccionario para almacenar los chunks cargados y sus entidades
loaded_chunks = {} # Formato: (chunk_x, chunk_z) -> [lista de entidades Ursina]

# --- Voxel para Interacción ---
class Voxel(Button):
    def __init__(self, position=(0,0,0), input_color=color.white):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5, # Hace que el origen sea la base del cubo
            texture='white_cube', # Una textura simple para el cubo
            color=input_color,
            highlight_color=color.lime, # Color cuando el mouse pasa por encima
            scale=1 # Tamaño del bloque
        )
    
    # Evento cuando se hace clic en un voxel
    def input(self, key):
        if self.hovered: # Si el mouse está sobre este voxel
            if key == 'left mouse down': # Clic izquierdo para destruir
                destroy(self) # Elimina el voxel de la escena
                # En un juego completo, aquí se actualizaría una matriz de mundo en memoria
            if key == 'right mouse down': # Clic derecho para colocar
                # Coloca un nuevo bloque encima del que estamos apuntando
                # Usamos un color por defecto para el bloque colocado
                new_voxel_pos = self.position + mouse.normal # mouse.normal es la cara del bloque a la que apuntamos
                Voxel(position=new_voxel_pos, input_color=color.gray) 

# --- Gestión de Chunks ---
def load_chunk(cx, cz):
    if (cx, cz) in loaded_chunks:
        return # Chunk ya cargado

    # print(f"Cargando chunk: ({cx}, {cz})") # Comentar para menos spam en consola
    chunk_entities = []
    
    # Genera los datos del chunk usando Numerium
    voxel_data = generate_numerium_chunk(GLOBAL_SEED, cx, cz, CHUNK_SIZE, CHUNK_SIZE, MAX_Y_HEIGHT)
    
    # Crea las entidades Ursina para cada voxel generado
    for voxel_info in voxel_data:
        voxel = Voxel(position=voxel_info['pos'], input_color=voxel_info['color'])
        chunk_entities.append(voxel)
    
    loaded_chunks[(cx, cz)] = chunk_entities

def unload_chunk(cx, cz):
    if (cx, cz) not in loaded_chunks:
        return # Chunk no cargado
    
    # print(f"Descargando chunk: ({cx}, {cz})") # Comentar para menos spam en consola
    for entity in loaded_chunks[(cx, cz)]:
        destroy(entity) # Elimina la entidad de la escena
    del loaded_chunks[(cx, cz)]

# --- Configuración del Jugador ---
player = FirstPersonController(
    model='cube', # Un modelo simple para el jugador
    collider='box', # Un colisionador de caja
    position=(0, MAX_Y_HEIGHT + 2, 0) # Empieza por encima del mundo para no caer
)
# Opcional: ajustar la velocidad del jugador
player.speed = 10 

# Una pequeña plataforma inicial para el jugador
Entity(model='cube', scale=(2,1,2), position=(0,-1,0), color=color.dark_gray, collider='box', texture='white_cube')




# Función para actualizar los chunks basados en la posición del jugador
# Se llama solo cuando el jugador cambia de chunk
def update_chunks_based_on_player_pos(current_player_chunk_x, current_player_chunk_z):
    # Identifica los chunks que deberían estar cargados
    chunks_to_load = set()
    for dx in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
        for dz in range(-RENDER_DISTANCE, RENDER_DISTANCE + 1):
            chunks_to_load.add((current_player_chunk_x + dx, current_player_chunk_z + dz))
# Llamada inicial para cargar los chunks alrededor del punto de inicio del jugador
# La posición del jugador puede estar en coordenadas flotantes, así que usamos floor
            update_chunks_based_on_player_pos(
    math.floor(player.x / CHUNK_SIZE),
    math.floor(player.z / CHUNK_SIZE)
)
    # Carga nuevos chunks
    for cx, cz in chunks_to_load:
        load_chunk(cx, cz)

    # Descarga chunks que están fuera del rango
    chunks_to_unload = [
        (cx, cz) for (cx, cz) in loaded_chunks.keys() 
        if (cx, cz) not in chunks_to_load
    ]
    for cx, cz in chunks_to_unload:
        unload_chunk(cx, cz)

# --- Bucle de Actualización del Juego (llamado cada frame por Ursina) ---
last_player_chunk_coords = (math.floor(player.x / CHUNK_SIZE), math.floor(player.z / CHUNK_SIZE))

def update():
    global last_player_chunk_coords
    
    # Actualiza los chunks solo si el jugador se ha movido a un nuevo chunk
    current_player_chunk_coords = (math.floor(player.x / CHUNK_SIZE), math.floor(player.z / CHUNK_SIZE))

    if current_player_chunk_coords != last_player_chunk_coords:
        update_chunks_based_on_player_pos(current_player_chunk_coords[0], current_player_chunk_coords[1])
        last_player_chunk_coords = current_player_chunk_coords

# --- Inicio del Juego ---
# Para asegurarse de que la aplicación Ursina se cierre correctamente al cerrar la ventana.
# application.development_mode = False # Puedes comentar esto si quieres más depuración de Ursina
# application.base.win.set_close_callback(on_quit) # Esto es para el cierre limpio, sys.exit es más forzado

app.run()
