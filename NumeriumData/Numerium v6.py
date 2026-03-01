from ursina import *
import numpy as np # Todavía lo necesitamos para el array de posiciones

# --- Configuración Base ---
N_CHUNK_SIZE = 16
MAX_HEIGHT = 5 # Altura máxima muy pequeña para empezar
# BASE_NUMERIUM y GLOBAL_SEED no se usarán en esta versión simplificada

# --- Funciones de Color ---
def get_simple_color(x, z):
    """Solo para probar: asigna un color basado en la posición para ver si funcionan los cubos."""
    if (x + z) % 2 == 0:
        return color.red
    else:
        return color.blue

# --- Generación de Cubos Simplificada ---
def generate_test_cubes():
    print("Generando cubos de prueba...")
    
    # Usaremos una matriz muy simple para verificar si hay un bloque
    # Asumiremos que solo colocamos bloques en el nivel Y=0 por ahora
    test_occupied_positions = np.full((N_CHUNK_SIZE, N_CHUNK_SIZE), False, dtype=bool)

    for z_local in range(N_CHUNK_SIZE):
        for x_local in range(N_CHUNK_SIZE):
            # Posición en el mundo
            x_global = x_local
            z_global = z_local
            y_height = 0 # Siempre colocamos en Y=0

            # Intentamos colocar un bloque si la posición no está ocupada
            if not test_occupied_positions[x_local, z_local]:
                test_occupied_positions[x_local, z_local] = True
                
                block_color = get_simple_color(x_local, z_local)

                Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, y_height, z_global),
                    scale=1,
                    parent=scene,
                    shader=lit_shader # Usamos lit_shader para ver la iluminación
                )
    print("Cubos de prueba generados.")


# --- Configuración de Ursina ---
app = Ursina()

# --- Configuración de la Ventana y Fondo ---
window.color = color.rgb(70, 100, 120) # Un azul cielo oscuro para mejor contraste

# --- Iluminación: CRUCIAL para que los objetos con lit_shader sean visibles ---
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1)) # Luz desde arriba a la derecha
AmbientLight(color=color.rgba(70, 70, 70, 255)) # Luz ambiental tenue

# --- Configuración de Cámara ---
EditorCamera() 
camera.orthographic = True 
# Ajustamos la posición para ver un plano de 16x16 desde arriba
camera.position = (N_CHUNK_SIZE / 2, N_CHUNK_SIZE * 1.5, -N_CHUNK_SIZE / 2) 
camera.rotation_x = -45 
camera.fov = N_CHUNK_SIZE * 1.5 

# --- Generar los Cubos de Prueba ---
generate_test_cubes()

# --- Bucle principal de Ursina ---
app.run()