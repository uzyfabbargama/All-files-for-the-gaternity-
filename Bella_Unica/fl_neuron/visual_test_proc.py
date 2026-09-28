import pygame
import sys

# ============================================================
# CONFIGURACIÓN EDITABLE (cambia aquí A y B)
# ============================================================
A_BITS = "0010110010101110"   # 16 bits visibles de A
B_BITS = "0110110010101110"   # 16 bits visibles de B
# ============================================================

# --- Lógica de 56 bits (fiel a test_proc.py) ---
BITS_TOTAL = 56
FRAC_BITS = 55

def float_to_custom56(val: float) -> int:
    entero = 1 if val >= 1.0 else 0
    frac = val - entero
    frac_bits = int(frac * (2 ** FRAC_BITS))
    return (entero << FRAC_BITS) | (frac_bits & ((1 << FRAC_BITS) - 1))

def custom56_to_float(val_int: int) -> float:
    entero = (int(val_int) >> int(FRAC_BITS)) & 1
    frac_bits = int(val_int) & ((1 << FRAC_BITS) - 1)
    return entero + (frac_bits / (2 ** FRAC_BITS))

def bits16_to_float56(bits16: str) -> int:
    """Convierte 16 bits visibles en un entero de 56 bits.
    Los 16 bits se colocan en la parte ALTA de la fracción (bits 54..39),
    y el resto (bits 38..0) se rellenan con un patrón pseudoaleatorio
    determinista para simular los 40 bits bajos."""
    assert len(bits16) == 16
    frac_high = int(bits16, 2)  # 16 bits
    # Colocamos los 16 bits en la parte alta de la fracción de 55 bits
    frac = (frac_high << (FRAC_BITS - 16)) & ((1 << FRAC_BITS) - 1)
    # Relleno determinista de los bits bajos con un LFSR simple
    seed = frac_high if frac_high != 0 else 0xACE1
    low = 0
    for i in range(FRAC_BITS - 16):
        seed = ((seed << 1) ^ ((seed >> 15) & 1)) & 0xFFFF
        low = (low << 1) | (seed & 1)
    frac |= low
    return frac  # entero = 0

def procesar_neurona_56(r12: int, r13: int):
    r15 = 0
    r15 = (r15 | r12) & 0xFFFFFFFFFFFFFFFF
    r15 = (r15 & r13) & 0xFFFFFFFFFFFFFFFF
    r12 = (r12 + r15) & 0xFFFFFFFFFFFFFFFF
    r13 = (r13 + r15) & 0xFFFFFFFFFFFFFFFF
    r13_before = r13
    r13 = (r13 + r12) & 0xFFFFFFFFFFFFFFFF
    carry_info = detectar_acarreo(r13_before, r12, r13)
    r15 = (r15 + r13) & 0xFFFFFFFFFFFFFFFF
    r15 = (r15 << 1) & 0xFFFFFFFFFFFFFFFF
    r15 = (r15 >> FRAC_BITS) & 0xFFFFFFFFFFFFFFFF
    r15 = (r15 & 1) & 0xFFFFFFFFFFFFFFFF
    r9 = r15 & 0xFF
    val_resultado = custom56_to_float(r13 & ((1 << BITS_TOTAL) - 1))
    return r9, val_resultado, r13, carry_info

def detectar_acarreo(a: int, b: int, resultado: int):
    """Devuelve una lista de 56 booleanos: True si en esa posición hubo acarreo
    generado o propagado durante a + b."""
    carries = [False] * BITS_TOTAL
    carry = 0
    for i in range(BITS_TOTAL):
        bit_a = (a >> i) & 1
        bit_b = (b >> i) & 1
        s = bit_a + bit_b + carry
        if s >= 2:
            carries[i] = True
            carry = 1
        else:
            carry = 0
    return carries

# --- Preparar datos ---
r12 = bits16_to_float56(A_BITS)
r13 = bits16_to_float56(B_BITS)
r9, val_c, r13_final, carry_info = procesar_neurona_56(r12, r13)
val_a = custom56_to_float(r12)
val_b = custom56_to_float(r13_final if False else custom56_to_float(r13))

# Recalcular B original (antes del proc) para mostrar
r13_orig = bits16_to_float56(B_BITS)
val_b = custom56_to_float(r13_orig)

# --- Pygame ---
pygame.init()
WIDTH, HEIGHT = 1100, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ondas binarias A / B / C — resonancia y acarreo")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 16)
font_small = pygame.font.SysFont("monospace", 13)

# Colores
BG = (15, 15, 25)
LANE = (40, 40, 60)
BIT1 = (80, 200, 255)
BIT0 = (255, 120, 120)
LINE = (90, 90, 130)
CARRY = (255, 200, 60)
FIRE_ON = (80, 255, 120)
FIRE_OFF = (255, 70, 70)
TEXT = (220, 220, 230)
TEXT_DIM = (150, 150, 170)

# Layout
MARGIN_LEFT = 180
MARGIN_RIGHT = 180
LANE_Y = [120, 280, 440]
LANE_NAMES = ["A", "B", "C"]
BIT_W = (WIDTH - MARGIN_LEFT - MARGIN_RIGHT) // 16
AMP = 45
DOT_R = 6

def bits_de_56(entero: int, n: int = 16):
    """Extrae los n bits más significativos de la fracción (bits 54..39)."""
    frac = entero & ((1 << FRAC_BITS) - 1)
    return [(frac >> (FRAC_BITS - 1 - i)) & 1 for i in range(n)]

bits_a = bits_de_56(r12, 16)
bits_b = bits_de_56(r13_orig, 16)
bits_c = bits_de_56(r13_final, 16)

# Carries relevantes para los 16 bits visibles (bits 39..54)
carry_vis = [carry_info[FRAC_BITS - 1 - i] for i in range(16)]

def draw_lane(y, bits, name, color_bits=(BIT1, BIT0), carries=None):
    # Línea base del carril
    pygame.draw.line(screen, LANE, (MARGIN_LEFT - 30, y), (WIDTH - MARGIN_RIGHT + 30, y), 1)
    # Nombre
    label = font.render(name, True, TEXT)
    screen.blit(label, (40, y - 10))
    # Puntos
    pts = []
    for i, b in enumerate(bits):
        x = MARGIN_LEFT + i * BIT_W + BIT_W // 2
        yy = y - AMP if b == 1 else y + AMP
        pts.append((x, yy))
    # Líneas entre puntos
    for i in range(len(pts) - 1):
        pygame.draw.line(screen, LINE, pts[i], pts[i+1], 2)
    # Puntos
    for i, (x, yy) in enumerate(pts):
        c = color_bits[0] if bits[i] == 1 else color_bits[1]
        if carries and carries[i]:
            pygame.draw.circle(screen, CARRY, (x, yy), DOT_R + 4, 0)
        pygame.draw.circle(screen, c, (x, yy), DOT_R)
        pygame.draw.circle(screen, (0, 0, 0), (x, yy), DOT_R, 1)

# --- Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    screen.fill(BG)

    # Título
    title = font.render("Resonancia binaria: A & B → C  (16 bits visibles de 56)", True, TEXT)
    screen.blit(title, (30, 20))

    # Carriles
    draw_lane(LANE_Y[0], bits_a, "A")
    draw_lane(LANE_Y[1], bits_b, "B")
    draw_lane(LANE_Y[2], bits_c, "C", carries=carry_vis)

    # Texto de valores
    lines = [
        f"A = {val_a:.12f}   bits: {A_BITS}",
        f"B = {val_b:.12f}   bits: {B_BITS}",
        f"C = {val_c:.12f}",
        f"Disparo r9 = {r9}",
    ]
    for i, t in enumerate(lines):
        col = FIRE_ON if (i == 3 and r9 == 1) else (FIRE_OFF if i == 3 else TEXT)
        screen.blit(font.render(t, True, col), (30, 500 + i * 20))

    # Indicador de disparo
    fire_x = WIDTH - 120
    fire_y = 120
    fire_color = FIRE_ON if r9 == 1 else FIRE_OFF
    pygame.draw.circle(screen, fire_color, (fire_x, fire_y), 35)
    pygame.draw.circle(screen, (0, 0, 0), (fire_x, fire_y), 35, 2)
    lab = font.render(f"r9={r9}", True, (0, 0, 0))
    screen.blit(lab, (fire_x - 25, fire_y - 8))

    # Leyenda de acarreo
    pygame.draw.circle(screen, CARRY, (WIDTH - 160, 200), 8)
    screen.blit(font_small.render("acarreo", True, TEXT_DIM), (WIDTH - 140, 192))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
