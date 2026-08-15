import pygame

# Tu paleta maestra de 8 bits
PALETTE_RGB = {
    "blanco": (255, 255, 255),
    "rojo": (255, 0, 0),
    "verde": (0, 255, 0),
    "azul": (0, 0, 255),
    "negro": (0, 0, 0),
    "verde rojo": (128, 128, 0),
    "azul rojo": (128, 0, 128),
    "azul verde": (0, 128, 128),
    "blanco rojo verde rojo": (200, 100, 100)
}

def get_sequence(bits):
    # Tu lógica de lol.py pero devolviendo colores RGB
    # (Adaptación de tu función rules)
    colors = []
    i = 0
    while i < len(bits):
        if bits[i] == '0':
            colors.append(PALETTE_RGB["negro"])
            i += 1
        else:
            start = i
            while i < len(bits) and bits[i] == '1':
                i += 1
            count = i - start
            # Mapeo según tus reglas de lol.py
            keys = {1:"blanco", 2:"rojo", 3:"verde", 4:"azul", 
                    5:"verde rojo", 6:"azul rojo", 7:"azul verde", 8:"blanco rojo verde rojo"}
            colors.append(PALETTE_RGB.get(keys.get(count), (255, 255, 0)))
    return colors

# En el bucle de Pygame:
# 1. Tomas un byte (0-255).
# 2. Sacas su secuencia con get_sequence(bin(byte)[2:].zfill(8)).
# 3. Dibujas cada color de la secuencia en una ráfaga de tiempo o espacio.
# --- INICIALIZACIÓN DE PYGAME ---
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Visualizador de Transurgencia de Bytes")
clock = pygame.time.Clock()

byte_actual = 0

# --- BUCLE PRINCIPAL ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30)) # Fondo oscuro (Lubuntu style)

    # Convertimos el byte actual a bits y obtenemos los colores
    bits = bin(byte_actual)[2:].zfill(8)
    secuencia_colores = get_sequence(bits)

    # Dibujamos la secuencia en pantalla
    for idx, color in enumerate(secuencia_colores):
        rect_width = 800 // len(secuencia_colores)
        pygame.draw.rect(screen, color, (idx * rect_width, 200, rect_width, 200))

    # Ciclo de bytes (0 a 255)
    byte_actual = (byte_actual + 1) % 256

    pygame.display.flip()
    clock.tick(10) # 10 actualizaciones por segundo para que sea visible

pygame.quit()
sys.exit()
