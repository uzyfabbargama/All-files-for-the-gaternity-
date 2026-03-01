# --- CONFIGURACIÓN ESTRUCTURAL ---
bits = 15
base = 1 << bits # 32768
mask = base - 1 

# Posiciones de registros y controladores
PosZ, PosC = 0, bits
PosY, PosC1 = bits + 1, (bits * 2) + 1
PosX, PosC2 = (bits * 2) + 2, (bits * 3) + 2

# --- MOTOR DE EXPERIENCIA (Subconsciente) ---
def Numeraso_Exp(ExpX, ExpY, ExpZ):
    # Construcción del numeraso de experiencia
    NumerasoXP = (ExpX*PosX) + (ExpY*PosY) + (ExpZ*PosZ) + PosC + PosC1 + PosC2
    C1 = (NumerasoXP // PosC) % 2 
    C2 = (NumerasoXP // PosC1) % 2 
    C3 = (NumerasoXP // PosC2) % 2 
    caso = C1 + C2 + C3 
    
    while caso != 3:
        D1, D2, D3 = 1 - C1, 1 - C2, 1 - C3
        NumerasoXP += D1 * PosC + D2 * PosC1 + D3 * PosC2 
        NumerasoXP += D1 - (D1*PosY) - (D2*PosZ) - (D3*PosX) # Equilibrio fractal
        C1 = (NumerasoXP // PosC) % 2 
        C2 = (NumerasoXP // PosC1) % 2 
        C3 = (NumerasoXP // PosC2) % 2 
        caso = C1 + C2 + C3
        
    return int((NumerasoXP // PosX) % base), int((NumerasoXP // PosY) % base), int((NumerasoXP // PosZ) % base)

# --- LÓGICA DE LA NEURONA (Consciencia Aritmética) ---
def Numeraso2_update(expx, expy, expz, Numero_generado):
    C4 = (Numero_generado >> PosC) & 1
    C5 = (Numero_generado >> PosC1) & 1
    C6 = (Numero_generado >> PosC2) & 1
    caso = C4 + C5 + C6
    
    # Sincronización con el motor de experiencia
    expx, expy, expz = Numeraso_Exp(expx, expy, expz)
    
    while caso != 3:
        D4, D5, D6 = 1 - C4, 1 - C5, 1 - C6
        expz += D4; expy += D5; expx += D6
        
        # Inyección de energía branchless
        Numero_generado += (D4 << PosZ) + (D4 << PosC) + (D5 << PosC1) + (D6 << PosC2)
        Numero_generado += (D4*expx) << PosZ
        Numero_generado -= (D4*expx) << PosY
        Numero_generado -= ((D5*expy) << PosZ) - ((D5*expy) << PosX)
        Numero_generado -= ((D6*expz) << PosX) - ((D6*expz) << PosY)
        
        # Recalcular controladores
        C4 = (Numero_generado >> PosC2) & 1
        C5 = (Numero_generado >> PosC1) & 1
        C6 = (Numero_generado >> PosC) & 1
        caso = C4 + C5 + C6
        
        # Conservación emocional (la curva de aprendizaje)
        Numero_generado += int(D4*(base/(expz+1))%base + D5*(base/(expy+1))%base + D6*(base/(expx+1))%base)
        Numero_generado %= ((base**3) * 2**3)
        
    return Numero_generado, expx, expy, expz

# --- EL "OJO" Y EL ENJAMBRE ---
def xorid(fragmento):
    id_acc = 0
    for car in fragmento:
        id_acc = (id_acc ^ ord(car)) << 1
    return id_acc

# Inicialización
num_n = 256
memoria = [(0 << PosX) + (0 << PosY) + (0 << PosZ) + PosC + PosC1 + PosC2 for _ in range(num_n)]
exps = [[0, 0, 0] for _ in range(num_n)]

def procesar(texto):
    for i in range(0, len(texto), 8):
        frag = texto[i:i+8]
        idx = xorid(frag) % num_n
        
        res, ex0, ex1, ex2 = Numeraso2_update(exps[idx][0], exps[idx][1], exps[idx][2], memoria[idx])
        memoria[idx], exps[idx] = res, [ex0, ex1, ex2]
    print("Procesamiento completado.")
