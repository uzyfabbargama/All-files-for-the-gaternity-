# ==============================================================================
# CUT THE AD: MOTOR DE TRES PASADAS Y REGLA DE AGARRE (PYTHON PURO)
# Cero dependencias externas. Trabaja directamente sobre matrices de bytes.
# ==============================================================================

def procesar_anuncio_3_pasadas(matriz_rgba, width, height):
    """
    Entrada: Matriz de píxeles RGBA (tu buffer de 24/32 bits)
    Salida: Mapa de filos (0 a 7)
    """
    # --------------------------------------------------------------------------
    # PASO 1: Reducción de 32/24 bits a Máscara Binaria (0 o 1)
    # --------------------------------------------------------------------------
    # Puntuamos 1 si el canal Alpha/visibilidad está activo, 0 si es transparente
    mascara_1 = [[0] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            # Simulamos verificación del canal Alpha
            mascara_1[y][x] = 1 if matriz_rgba[y][x] != '.' else 0

    # --------------------------------------------------------------------------
    # PASO 2: Identificación de Bordes (Superficie = 2)
    # --------------------------------------------------------------------------
    # Un píxel '1' se convierte en '2' si tiene al menos un vecino transparente '0'
    mascara_2 = [[0] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if mascara_1[y][x] == 1:
                vecinos_vacios_4dir = (
                    mascara_1[y - 1][x] == 0 or
                    mascara_1[y + 1][x] == 0 or
                    mascara_1[y][x - 1] == 0 or
                    mascara_1[y][x + 1] == 0
                )
                if vecinos_vacios_4dir:
                    mascara_2[y][x] = 2  # Marcado como borde/superficie

    # --------------------------------------------------------------------------
    # PASO 3: Cálculo de Filo (1 a 7) y Autolimpieza Bitwise (vecinos & 7)
    # --------------------------------------------------------------------------
    mapa_filos = [[0] * width for _ in range(height)]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            if mascara_2[y][x] == 2:
                # Contamos los 8 vecinos transparentes en la máscara original
                vecinos_vacios = 0
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        if mascara_1[y + dy][x + dx] == 0:
                            vecinos_vacios += 1
                
                # Truco binario: (vecinos_vacios & 7)
                # Si está aislado (8 vecinos vacíos): 8 & 7 = 0 -> Se auto-elimina
                filo = vecinos_vacios & 7
                mapa_filos[y][x] = filo

    return mascara_1, mascara_2, mapa_filos

# ==============================================================================
# DEMO Y SIMULACIÓN DE REGLAS DE JUEGO EN TERMINAL
# ==============================================================================

# Representación ASCII de un anuncio ('.' = Transparente, '#' = Objeto visible)
# Tiene una punta súper afilada a la derecha y bordes planos
ANUNCIO_ASCII = [
    "...................................",
    ".....#################.............",
    ".....####################..........",
    ".....#######################.......",
    ".....##########################....",  # <--- Punta afilada
    ".....#######################.......",
    ".....####################..........",
    ".....#################.............",
    "..................................."
]

HEIGHT = len(ANUNCIO_ASCII)
WIDTH = len(ANUNCIO_ASCII[0])

# 1. Ejecutar las 3 Pasadas
m1, m2, mapa_filos = procesar_anuncio_3_pasadas(ANUNCIO_ASCII, WIDTH, HEIGHT)

print("\n--- PASO 1: MÁSCARA BINARIA (0/1) ---")
for row in m1:
    print("".join(str(cell) if cell else " " for cell in row))

print("\n--- PASO 2: BORDES IDENTIFICADOS (2) ---")
for row in m2:
    print("".join(str(cell) if cell else " " for cell in row))

print("\n--- PASO 3: MAPA DE FILOS FINAL (1-7) ---")
# Coloreamos la terminal con códigos ANSI: Verde = Seguro (<=3), Rojo = Cortante (>3)
for y in range(HEIGHT):
    linea = ""
    for x in range(WIDTH):
        f = mapa_filos[y][x]
        if f == 0:
            linea += " "
        elif f > 3:
            # Rojo para filos peligrosos (> 3)
            linea += f"\033[91m{f}\033[0m"
        else:
            # Verde para agarres seguros (<= 3)
            linea += f"\033[92m{f}\033[0m"
    print(linea)

# 2. Simulación de la Regla de Agarre / Daño
print("\n==================================================")
print("     SIMULACIÓN DE REGLA DE AGARRE DEL JUGADOR    ")
print("==================================================")

puntos_de_prueba = [
    (10, 2, "Borde Superior Plano"),
    (29, 4, "Punta Afilada de la Derecha"),
    (12, 4, "Relleno Interno (Sin filo)")
]

vida_jugador = 100

for x, y, desc in puntos_de_prueba:
    filo = mapa_filos[y][x]
    print(f"\nJugador intenta agarrar en X:{x}, Y:{y} ({desc}):")
    print(f" -> Nivel de Filo detectado: {filo}")
    
    if filo > 3:
        daño = (filo - 3) * 15
        vida_jugador -= daño
        print(f" -> \033[91m¡CORTE DETECTADO! Recibes {daño} de daño.\033[0m Vida restante: {vida_jugador} HP")
    elif filo > 0:
        print(f" -> \033[92mAgarre seguro.\033[0m Puedes levantar o mover esta pieza sin hacerte daño.")
    else:
        print(" -> Tocando superficie plana o relleno. No hay filo en este punto.")
