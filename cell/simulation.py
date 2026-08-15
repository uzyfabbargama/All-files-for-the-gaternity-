import pygame
import numpy as np

# Configuración ligera para el Athlon
RES = 32
PIXEL_SIZE = 30
WIDTH = RES * PIXEL_SIZE
HEIGHT = RES * PIXEL_SIZE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Micro-Transurgencia Interactiva 16x16")
clock = pygame.time.Clock()

# Universo inicial (Todo 0, excepto el centro)
universo = np.zeros((RES, RES), dtype=np.uint8)
universo[0, 1] = 0xFE  # Tu "Fiat Lux": add rax, 1
universo[0, 0] = 0xFF
universo[1, 1] = 0xFD
def update_logic(grid):
    new_grid = grid.copy()
    padded_grid = np.pad(grid, 1, mode='wrap')
    for y in range(1, RES+1): #antes era -
        for x in range(1, RES+1): #también
            # Simulando tu macro update_cell (UP y CENTER)
            up = padded_grid[y-1, x]
            center = padded_grid[y, x]
            # La asimetría "right, right" que descubrimos
            right = padded_grid[y, x+1]
            
            # Lógica XOR de transurgencia
            diff = up ^ center
            
            # El efecto "right, right" como inyector de energía
            # (Simulamos la suma asimétrica que mencionamos)
            nuevo_val = np.add((center ^ diff), (right & 1), dtype=np.uint8)
            # Forzamos a que la suma se comporte como un byte de hardware
            new_grid[y-1, x-1] = nuevo_val
            
    return new_grid
paused = True   # Empezamos en pausa
running = True
while running:
    screen.fill((0, 0, 30)) # Azul profundo (espacio)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        # --- Control de Pausa ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                print(f"Simulación {'Pausada' if paused else 'Corriendo'}")

        # --- DETECCIÓN DE CLICK PARA INYECTAR ENERGÍA ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Click izquierdo
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Calcular la celda correspondiente
                cell_x = mouse_x // PIXEL_SIZE
                cell_y = mouse_y // PIXEL_SIZE
                
                # Asegurarnos de que está dentro de los límites
                if 0 <= cell_x < RES and 0 <= cell_y < RES:
                    # Inyectar energía (+1) con control de overflow
                    current_val = universo[cell_y, cell_x]
                    # Volvemos a usar np.add para que sea "estilo hardware"
                    new_val = np.add(current_val, 1, dtype=np.uint8)
                    universo[cell_y, cell_x] = new_val
                    print(f"Inyectada energía en ({cell_x}, {cell_y}): {current_val} -> {new_val}")
    if not paused:
        universo = update_logic(universo)

    # Dibujar la "Piel" y los "Bits"
    for y in range(RES):
        for x in range(RES):
            val = universo[y, x]
            # Color mejorado
            if val == 0:
                color = (0, 0, 50) # Vacío
            elif val < 64:
                color = (0, 0, 180) # Azul (poca energía)
            elif val < 128:
                color = (0, 180, 0) # Verde
            elif val < 192:
                color = (220, 0, 0) # Rojo
            else:
                color = (220, 0, 220) # Magenta (mucha energía)
            
            rect = pygame.Rect(x*PIXEL_SIZE, y*PIXEL_SIZE, PIXEL_SIZE-1, PIXEL_SIZE-1)
            pygame.draw.rect(screen, color, rect)
            
            # Dibujar los 8 bits como puntitos blancos/negros
            for i in range(8):
                bit = (val >> (7-i)) & 1
                bit_color = (255, 255, 255) if bit else (0, 0, 0)
                pygame.draw.rect(screen, bit_color, (x*PIXEL_SIZE + (i*3) + 2, y*PIXEL_SIZE + 12, 2, 2))
    # --- Instrucciones en pantalla ---
    font = pygame.font.SysFont(None, 20)
    text_pause = font.render("[ESPACIO] Pausa/Correr", True, (255, 255, 255))
    text_click = font.render("[CLICK IZQ] +1 Energía", True, (255, 255, 255))
    text_status = font.render(f"Estado: {'PAUSADO' if paused else 'CORRIENDO'}", True, (0, 255, 0) if not paused else (255, 0, 0))
    
    screen.blit(text_pause, (10, HEIGHT - 60))
    screen.blit(text_click, (10, HEIGHT - 40))
    screen.blit(text_status, (10, HEIGHT - 20))
    pygame.display.flip()
    clock.tick(5) # 5 "años" por segundo para poder observar el plegado

pygame.quit()
