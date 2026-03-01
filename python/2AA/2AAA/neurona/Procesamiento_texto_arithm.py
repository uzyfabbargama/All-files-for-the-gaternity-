# ==========================================
# BELLA: NÚCLEO ARITMÉTICO UNIFICADO (3 KiB)
# ==========================================

# Parámetros del Sistema
bits = 15
base = 1 << bits  # 32768
PosZ, PosC = 0, bits
PosY, PosC1 = bits + 1, (bits * 2) + 1
PosX, PosC2 = (bits * 2) + 2, (bits * 3) + 2

# 1. MOTOR DE EXPERIENCIA (Numeraso_Exp.py)
def Numeraso_Exp(ExpX, ExpY, ExpZ):
    NumerasoXP = (ExpX*PosX) + (ExpY*PosY) + (ExpZ*PosZ) + PosC + PosC1 + PosC2
    C1 = (NumerasoXP >> PosC) & 1
    C2 = (NumerasoXP >> PosC1) & 1
    C3 = (NumerasoXP >> PosC2) & 1
    caso = C1 + C2 + C3
    while caso != 3:
        D1, D2, D3 = 1 - C1, 1 - C2, 1 - C3
        NumerasoXP += (D1 << PosC) + (D2 << PosC1) + (D3 << PosC2)
        NumerasoXP += D1 - (D1<<PosY) - (D2<<PosZ) - (D3<<PosX)
        C1, C2, C3 = (NumerasoXP >> PosC) & 1, (NumerasoXP >> PosC1) & 1, (NumerasoXP >> PosC2) & 1
        caso = C1 + C2 + C3
    return int((NumerasoXP >> PosX) % base), int((NumerasoXP >> PosY) % base), int((NumerasoXP >> PosZ) % base)

# 2. LÓGICA DE NEURONA (Neuron.py)
def Numeraso2_update(expx, expy, expz, Numero_generado):
    C4 = (Numero_generado >> PosC) & 1
    C5 = (Numero_generado >> PosC1) & 1
    C6 = (Numero_generado >> PosC2) & 1
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
        C4 = (Numero_generado >> PosC) & 1  # Bit 15
        C5 = (Numero_generado >> PosC1) & 1 # Bit 31
        C6 = (Numero_generado >> PosC2) & 1 # Bit 47
        caso = C4 + C5 + C6
        Numero_generado += int(D4*(base/(expz+1))%base + D5*(base/(expy+1))%base + D6*(base/(expx+1))%base)
        Numero_generado %= ((base**3) * 2**3)
        Numero_generado = int(Numero_generado)
    return int(Numero_generado), expx, expy, expz

# 3. EL "OJO" (xor_id.py)
def xorid(fragmento):
    id_acc = 0
    for caracter in fragmento:
        id_acc = (id_acc ^ ord(caracter)) << 1
    return id_acc

# 4. EL ENJAMBRE (Test0.py)
num_neuronas = 256
memoria_bhl = [(0 << PosX) + (0 << PosY) + (0 << PosZ) + PosC + PosC1 + PosC2 for _ in range(num_neuronas)]
experiencias = [[0, 0, 0] for _ in range(num_neuronas)]

def procesar(texto):
    for i in range(0, len(texto), 8):
        frag = texto[i:i+8]
        idx = xorid(frag) % num_neuronas
        n_gen, ex0, ex1, ex2 = Numeraso2_update(experiencias[idx][0], experiencias[idx][1], experiencias[idx][2], memoria_bhl[idx])
        memoria_bhl[idx], experiencias[idx] = n_gen, [ex0, ex1, ex2]
    print("Bella ha procesado el texto.")
# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    frase = "hola pablo como estas" # 21 bytes (usará 3 bloques de 8 aprox)
    
    print(f"--- Iniciando Procesamiento de: '{frase}' ---")
    procesar(frase)
    
    # Vamos a ver qué pasó en el cerebro de 256 neuronas
    for i in range(num_neuronas):
        # Si la experiencia en Z, Y o X ya no es cero, algo cambió
        if sum(experiencias[i]) > 0:
            print(f"\n[Neurona {i}] detectó actividad:")
            print(f" > Numeraso (bin): {bin(memoria_bhl[i])}")
            print(f" > Experiencia (X,Y,Z): {experiencias[i]}")
