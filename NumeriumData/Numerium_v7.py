from ursina import *
from ursina.shaders import lit_shader # ¡IMPORTACIÓN NECESARIA PARA lit_shader!
import numpy as np 

# --- Configuración Base ---
N_CHUNK_SIZE = 16
MAX_HEIGHT = 5 

# --- Funciones de Color ---
def get_simple_color(x, z):
    if (x + z) % 2 == 0:
        return color.red
    else:
        return color.blue

# --- Generación de Cubos Simplificada ---
def generate_test_cubes():
    print("Generando cubos de prueba...")
    
    test_occupied_positions = np.full((N_CHUNK_SIZE, N_CHUNK_SIZE), False, dtype=bool)

    for z_local in range(N_CHUNK_SIZE):
        for x_local in range(N_CHUNK_SIZE):
            x_global = x_local
            z_global = z_local
            y_height = 0 

            if not test_occupied_positions[x_local, z_local]:
                test_occupied_positions[x_local, z_local] = True
                
                block_color = get_simple_color(x_local, z_local)

                Entity(
                    model='cube',
                    color=block_color,
                    position=(x_global, y_height, z_global),
                    scale=1,
                    parent=scene,
                    shader=lit_shader # ¡Ahora lit_shader estará definido!
                )
    print("Cubos de prueba generados.")


# --- Configuración de Ursina ---
app = Ursina()

# --- Configuración de la Ventana y Fondo ---
window.color = color.rgb(70, 100, 120) 

# --- Iluminación: CRUCIAL para que los objetos con lit_shader sean visibles ---
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1)) 
AmbientLight(color=color.rgba(70, 70, 70, 255)) 

# --- Configuración de Cámara ---
EditorCamera() 
camera.orthographic = True 
camera.position = (N_CHUNK_SIZE / 2, N_CHUNK_SIZE * 1.5, -N_CHUNK_SIZE / 2) 
camera.rotation_x = -45 
camera.fov = N_CHUNK_SIZE * 1.5 

# --- Generar los Cubos de Prueba ---
generate_test_cubes()

# --- Bucle principal de Ursina ---
app.run()