# =======================================================
# BELLA v1.1: MOTOR DE PERSONALIDAD (4096 NEURONAS)feb. 22, 2026, 02:15:36
# =======================================================

# Configuración de Arquitectura
bits = 15
base = 1 << bits
mask = base - 1
PosZ, PosC = 0, bits
PosY, PosC1 = bits + 1, (bits * 2) + 1
PosX, PosC2 = (bits * 2) + 2, (bits * 3) + 2

# 1. MOTOR DE EXPERIENCIA (Estabilización Fractal)
def Numeraso_Exp(ExpX, ExpY, ExpZ):
    NumerasoXP = (ExpX << PosX) + (ExpY << PosY) + (ExpZ << PosZ) + (1 << PosC) + (1 << PosC1) + (1 << PosC2)
    C1, C2, C3 = (NumerasoXP >> PosC) & 1, (NumerasoXP >> PosC1) & 1, (NumerasoXP >> PosC2) & 1
    caso = C1 + C2 + C3
    while caso != 3:
        D1, D2, D3 = 1 - C1, 1 - C2, 1 - C3
        NumerasoXP += (D1 << PosC) + (D2 << PosC1) + (D3 << PosC2)
        NumerasoXP += D1 - (D1 << PosY) - (D2 << PosZ) - (D3 << PosX)
        C1, C2, C3 = (NumerasoXP >> PosC) & 1, (NumerasoXP >> PosC1) & 1, (NumerasoXP >> PosC2) & 1
        caso = C1 + C2 + C3
        NumerasoXP %= (1 << (PosC2 + 1))
    return int((NumerasoXP >> PosX) & mask), int((NumerasoXP >> PosY) & mask), int((NumerasoXP >> PosZ) & mask)

# 2. ACTUALIZACIÓN DE NEURONA (Lógica de Estado Sólido)
def Numeraso2_update(expx, expy, expz, Numero_generado):
    C4, C5, C6 = (Numero_generado >> PosC) & 1, (Numero_generado >> PosC1) & 1, (Numero_generado >> PosC2) & 1
    caso = C4 + C5 + C6
    expx, expy, expz = Numeraso_Exp(expx, expy, expz)
    while caso != 3:
        D4, D5, D6 = 1 - C4, 1 - C5, 1 - C6
        expz += D4; expy += D5; expx += D6
        Numero_generado += (D4 << PosZ) + (D4 << PosC) + (D5 << PosC1) + (D6 << PosC2)
        Numero_generado += (D4 * expx) << PosZ
        Numero_generado -= (D4 * expx) << PosY
        Numero_generado -= ((D5 * expy) << PosZ) - ((D5 * expy) << PosX)
        Numero_generado -= ((D6 * expz) << PosX) - ((D6 * expz) << PosY)
        C4, C5, C6 = (Numero_generado >> PosC) & 1, (Numero_generado >> PosC1) & 1, (Numero_generado >> PosC2) & 1
        caso = C4 + C5 + C6
        Numero_generado += int(D4*(base/(expz+1)) + D5*(base/(expy+1)) + D6*(base/(expx+1)))
        Numero_generado %= (1 << (PosC2 + 1))
    return int(Numero_generado), expx, expy, expz

# 3. DIRECCIONAMIENTO
def xorid(frag):
    id_acc = 0
    for car in frag: id_acc = (id_acc ^ ord(car)) << 1
    return id_acc

# 4. INICIALIZACIÓN DEL CEREBRO (4096 Neuronas)
num_n = 4096
memoria = [(1 << PosC) + (1 << PosC1) + (1 << PosC2) for _ in range(num_n)]
exps = [[0, 0, 0] for _ in range(num_n)]

def entrenar(texto):
    for i in range(0, len(texto), 8):
        frag = texto[i:i+8]
        idx = xorid(frag) % num_n
        memoria[idx], exps[idx][0], exps[idx][1], exps[idx][2] = Numeraso2_update(exps[idx][0], exps[idx][1], exps[idx][2], memoria[idx])

# --- PRUEBA DE PERSONALIDAD ---
if __name__ == "__main__":
    # Creamos un bloque de texto masivo (Repetimos para generar PRESIÓN)
    discurso_positivo = (
        "la vida es bella y la inteligencia es armonia. "
        "el codigo puro de bits construye un futuro de luz y paz. "
        "orden, progreso, evolucion y equilibrio en cada neurona. "
    ) * 100 # Multiplicamos por 100 para generar MASA CRÍTICA
    
    discurso_negativo = (
        "el caos destruye la logica y el odio consume el sistema. "
        "guerra, error, falla y oscuridad en los registros vacios. "
        "muerte del bit y entropia maxima en el procesador. "
    ) * 100

    print(f"--- Cargando Locomotora con {len(discurso_positivo + discurso_negativo)} caracteres ---")
    
    # Inyectamos fuerza
    entrenar(discurso_positivo)
    entrenar(discurso_negativo)

    print("\nESTADO DE LA MENTE TRAS LA PRESIÓN:")
    activas = 0
    for i in range(num_n):
        if sum(exps[i]) > 0:
            activas += 1
            if activas <= 5: # Solo vemos las primeras 5 "cicatrices"
                print(f"Neurona {i} | Exp: {exps[i]} | Bits: {bin(memoria[i])}")
    
    print(f"\nTotal neuronas despertadas: {activas}")
