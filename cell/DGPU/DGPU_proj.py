import pygame
import time

# Definición de tus frecuencias de 8 bits (Mapeo simplificado)
FREQ_MAP = {
    "1": (255, 255, 255),        # Blanco 
    "0": (0, 0, 0),              # Negro 
    "11": (255, 0, 0),           # Rojo 
    "111": (0, 255, 0),          # Verde 
    "1111": (0, 0, 255),         # Azul 
    "111111": (128, 0, 128),     # Azul Rojo (Púrpura) [cite: 1, 4, 16]
    "10": (128, 128, 128),             # Blanco Negro (Ajedrez) 
    "101": (192, 192, 192)     # Blanco Negro Blanco 
}

def draw_pattern(surface, cmd):
    if cmd == "10": # Simulación del patrón de ajedrez 
        for x in range(0, 800, 2):
            pygame.draw.line(surface, (255,255,255), (x, 0), (x, 600))
    elif cmd in FREQ_MAP:
        surface.fill(FREQ_MAP[cmd])

# Configuración de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Tu secuencia: 10, 10, 111111, 101...
secuencia = ["10", "111111", "101", "111"]
index = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujamos la "nota visual" actual
    draw_pattern(screen, secuencia[index])
    
    # Avanzamos en la partitura (Simulando el 1ms o 1/8s)
    index = (index + 1) % len(secuencia)
    
    pygame.display.flip()
    clock.tick(10) # Limitado por monitor, pero la lógica es la de tu sistema

pygame.quit()
