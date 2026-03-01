import pygame
import os

# --- EL MOTOR XIP (TU ESTÁNDAR) ---
def xorid(palabra):
    id_acum = 0
    for char in palabra:
        id_acum = (id_acum ^ ord(char)) << 1
    return id_acum

def guardar_progreso_xip(archivo, datos):
    with open(archivo, "w", encoding="utf-8") as f:
        f.write("// --- XIP GAME SAVE ---\n")
        f.write("// Este archivo es generado por resonancia aritmética\n")
        for k, v in datos.items():
            f.write(f"{k} :: {v} ,,\n")

def cargar_progreso_xip(archivo):
    memoria = {}
    if not os.path.exists(archivo): return memoria
    with open(archivo, "r", encoding="utf-8") as f:
        for linea in f:
            limpia = linea.split("//")[0].strip()
            if not limpia or "::" not in limpia: continue
            bloques = limpia.split(",,")
            for b in bloques:
                if "::" not in b: continue
                k, v = b.split("::")
                memoria[xorid(k.strip())] = v.strip()
    return memoria

# --- CONFIGURACIÓN DEL JUEGO ---
pygame.init()
ventana = pygame.display.set_mode((600, 400))
pygame.display.set_caption("XIP-Runner Test")
clock = pygame.time.Clock()

# Variables del Jugador (Alias)
ID_X = xorid("pos_x")
ID_Y = xorid("pos_y")
ID_PUNTOS = xorid("puntos")

# Estado inicial
px, py = 300, 200
puntos = 0
archivo_save = "save_game.xip"

# CARGAR PROGRESO AL INICIO
print("[SISTEMA] Buscando sintonía con save_game.xip...")
mem = cargar_progreso_xip(archivo_save)
if ID_X in mem: px = int(mem[ID_X])
if ID_Y in mem: py = int(mem[ID_Y])
if ID_PUNTOS in mem: puntos = int(mem[ID_PUNTOS])

# --- BUCLE PRINCIPAL ---
ejecutando = True
while ejecutando:
    ventana.fill((30, 30, 30)) # Fondo oscuro
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_s: # PRESIONA 'S' PARA GUARDAR
                datos = {"pos_x": px, "pos_y": py, "puntos": puntos}
                guardar_progreso_xip(archivo_save, datos)
                print("[XIP] ¡Progreso sintonizado en el disco!")

    # Movimiento
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]: px -= 5
    if teclas[pygame.K_RIGHT]: px += 5
    if teclas[pygame.K_UP]: py -= 5
    if teclas[pygame.K_DOWN]: py += 5

    # Dibujar
    pygame.draw.rect(ventana, (0, 255, 150), (px, py, 40, 40)) # El jugador
    
    # Texto en pantalla
    fuente = pygame.font.SysFont("monospace", 15)
    img = fuente.render(f"PUNTOS: {puntos} | 'S' para Guardar con .xip", True, (255, 255, 255))
    ventana.blit(img, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
