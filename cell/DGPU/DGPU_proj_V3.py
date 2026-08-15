import pygame

# Mapeo de colores basado en tus reglas de 8 bits 
COLORS = {
    'blanco': (255, 255, 255), # 1 
    'negro': (0, 0, 0),        # 0 
    'rojo': (255, 0, 0),       # 11 
    'verde': (0, 255, 0),      # 111 
    'azul': (0, 0, 255)        # 1111 
}

# Patrones extraídos de tu lista DGPU 
PATTERNS = {
    "111111": ['azul', 'rojo', 'azul', 'rojo', 'azul', 'rojo'], # 
    "101101": ['blanco', 'negro', 'rojo', 'negro', 'blanco', 'negro'] # 
}

def draw_simulated_gpu(surface, pattern_key):
    pattern = PATTERNS.get(pattern_key, ['negro'])
    pixel_size = surface.get_width() // 256
    
    for y in range(256):
        for x in range(256):
            # El color depende de la posición y el patrón (SIMD extremo)
            color_idx = (x + y) % len(pattern)
            color_name = pattern[color_idx]
            pygame.draw.rect(surface, COLORS[color_name], 
                             (x * pixel_size, y * pixel_size, pixel_size, pixel_size))

# Configuración a 30 Hz como pediste
pygame.init()
size = 512 # 256 * 2 píxeles por cada píxel simulado
screen = pygame.display.set_mode((size, size))
clock = pygame.time.Clock()

current_pattern = "111111"

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
    
    draw_simulated_gpu(screen, current_pattern)
    pygame.display.flip()
    clock.tick(30) # Mitad de frecuencia para observar la lógica 

pygame.quit()
