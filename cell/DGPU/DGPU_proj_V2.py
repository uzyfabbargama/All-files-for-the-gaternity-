import pygame

# Mapeo basado en tu lista de 8 bits [cite: 1, 17]
FREQ_MAP = {
    "1": (255, 255, 255),        # Blanco [cite: 1]
    "0": (0, 0, 0),              # Negro [cite: 1]
    "11": (255, 0, 0),           # Rojo [cite: 1]
    "111": (0, 255, 0),          # Verde [cite: 1]
    "1111": (0, 0, 255),         # Azul [cite: 1]
    "111111": (128, 0, 128),     # Azul Rojo (Púrpura) 
    "11111111": (200, 50, 50),   # Blanco, Rojo, Verde, Rojo [cite: 1]
    "10": "ajedrez",             # PATRÓN: Blanco Negro [cite: 1]
    "101": "trama"               # PATRÓN: Blanco Negro Blanco [cite: 1]
}

def draw_pattern(surface, cmd):
    val = FREQ_MAP.get(cmd, (0, 0, 0))
    
    if val == "ajedrez":
        # SIMD: Llenamos con el patrón '10' [cite: 1]
        for x in range(0, surface.get_width(), 2):
            pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, surface.get_height()))
            pygame.draw.line(surface, (0, 0, 0), (x+1, 0), (x+1, surface.get_height()))
    
    elif val == "trama":
        # SIMD: Llenamos con el patrón '101' [cite: 1]
        for x in range(0, surface.get_width(), 3):
            pygame.draw.set_at((x, 0), (255, 255, 255)) # Blanco
            pygame.draw.set_at((x+1, 0), (0, 0, 0))     # Negro
            pygame.draw.set_at((x+2, 0), (255, 255, 255)) # Blanco
            # (En un monitor real esto se repetiría masivamente en 1ms) [cite: 1]
    
    else:
        # Es un color sólido de tu lista [cite: 1]
        surface.fill(val)

# --- Configuración Pygame ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Tu secuencia de prueba (1ms por paso) [cite: 1]
secuencia = ["10", "111111", "101", "111"] 
index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    # Dibujamos la instrucción de la DGPU [cite: 1]
    draw_pattern(screen, secuencia[index])
    
    index = (index + 1) % len(secuencia)
    
    pygame.display.flip()
    # A 60 FPS simulamos la persistencia, aunque tu monitor real iría a 1KHz [cite: 1]
    clock.tick(60) 

pygame.quit()
