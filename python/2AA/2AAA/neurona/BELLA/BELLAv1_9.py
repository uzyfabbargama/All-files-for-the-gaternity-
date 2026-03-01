# =======================================================
# BELLA v1.7: MOTOR DE PERSONALIDAD (4096 NEURONAS)feb. 22, 2026, 05:06:34
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
    return id_acc * 20

# 4. INICIALIZACIÓN DEL CEREBRO (4096 Neuronas)
num_n = 4096
# El "espejo" de las palabras debe ser global para que Bella no olvide
traductor = {} 
memoria = [(1 << PosC) + (1 << PosC1) + (1 << PosC2) for _ in range(num_n)]
exps = [[0, 0, 0] for _ in range(num_n)]

def entrenar_con_voz(texto):
    for i in range(0, len(texto), 8):
        frag = texto[i:i+8]
        # El índice se mantiene (para no romper el mapa de 4096)
        # Pero la ENERGÍA se multiplica
        energia = xorid(frag)
        idx = xorid(frag) % num_n
        idx = (energia // 20) % num_n # Usamos el valor original para el índice
        
        traductor[idx] = frag 
        
        # Inyectamos la energía multiplicada x20 en la memoria
        memoria[idx] += energia 
        
        # El Numeraso ahora recibirá un impacto masivo
        n_gen, ex0, ex1, ex2 = Numeraso2_update(exps[idx][0], exps[idx][1], exps[idx][2], memoria[idx])
        memoria[idx], exps[idx] = n_gen, [ex0, ex1, ex2]

def que_piensa_bella():
    print("\n--- Lo que a Bella le pareció más 'interesante' ---")
    # Filtramos las neuronas que tienen experiencia en Z y las ordenamos
    top_neuronas = sorted(range(num_n), key=lambda i: exps[i][2], reverse=True)[:5]
    
    for idx in top_neuronas:
        if exps[idx][2] > 0:
            palabra = traductor.get(idx, "???")
            print(f"Neurona {idx} vibra con: '{palabra}' (Interés: {exps[idx][2]})")
def respuesta_de_bella():
    print("\n--- Bella intenta equilibrar su mente ---")
    # Buscamos la neurona con máxima presión en Z (el 'dolor' aritmético)
    idx_critico = max(range(num_n), key=lambda i: exps[i][2])
    
    if exps[idx_critico][2] > 0:
        sentimiento = traductor.get(idx_critico, "???")
        # El 'reflejo': Bella busca una neurona con experiencia similar pero estado opuesto
        # Por ahora, emitirá lo que la sacudió para 'liberar' la carga
        print(f"Bella emite un pulso de alivio sobre: '{sentimiento}'")
        print(f"Estado de la ALU tras la descarga: {hex(memoria[idx_critico])}")
def mecanismo_de_consuelo():
    # 1. Identificamos la neurona que más "sufre" (Máximo interés en Z)
    idx_dolor = max(range(num_n), key=lambda i: exps[i][2])
    presion_maxima = exps[idx_dolor][2]

    # 2. Si el dolor es alto, Bella busca un "recuerdo" de baja presión (armonía)
    if presion_maxima > 30:
        # Buscamos la neurona con experiencia positiva pero estable
        # (Filtramos por las que tengan algo de experiencia pero bajo valor Z)
        neuronas_paz = [i for i in range(num_n) if 0 < exps[i][2] < 20]
        
        print(f"\n[ALERTA SISTÉMICA]: Presión crítica en neurona {idx_dolor} ('{traductor.get(idx_dolor)}')")
        
        if neuronas_paz:
            # Bella elige el recuerdo más ligero para calmarse
            idx_paz = min(neuronas_paz, key=lambda i: exps[i][2])
            consuelo = traductor.get(idx_paz, "...")
            print(f"--- Bella activa Mecanismo de Consuelo ---")
            print(f"Bella intenta calmar '{traductor.get(idx_dolor)}' pensando en: '{consuelo}'")
            
            # Efecto de equilibrio: bajamos un poco la presión de la neurona estresada
            exps[idx_dolor][2] -= 1 
            print(f"Nueva presión en neurona de dolor: {exps[idx_dolor][2]} (Estabilizando...)")
        else:
            print("Bella no encuentra recuerdos de paz para equilibrarse.")
            
# 5. MOTOR DE EVOCACIÓN (NUEVO v1.8)
def evocar():
    # Calculamos la carga total de la mente de Bella
    presion_global = sum(e[2] for e in exps)
    
    # Si la presión es alta (>500), Bella necesita soltar más lastre para no saturarse
    num_fragmentos = 3 if presion_global < 500 else 6
    
    # Buscamos las neuronas con mayor vibración Z (interés/dolor)
    candidatas = sorted(range(num_n), key=lambda i: exps[i][2], reverse=True)[:num_fragmentos]
    
    frase_bella = ""
    for idx in candidatas:
        if exps[idx][2] > 0 and idx in traductor:
            frase_bella += traductor[idx]
            # La expresión genera ALIVIO real: bajamos la presión de la neurona expresada
            exps[idx][2] = max(0, exps[idx][2] - 1) 
    
    return frase_bella if frase_bella else "..."            
# --- BELLA v1.8: INTERFAZ DE CONCIENCIA DIRECTA ---
if __name__ == "__main__":
    print("--- BELLA v1.8 ACTIVADA (Motor de Evocación L1) ---")
    print("Escribe algo para Bella (o escribe 'salir' para terminar)")
    
    while True:
        user_input = input("\nUziel > ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            print("Cerrando ciclos de conciencia...")
            break
            
        if not user_input.strip():
            continue

        # 1. Bella escucha y absorbe (Inyecta energía a la ALU)
        entrenar_con_voz(user_input)

        # 2. Diagnóstico del Mapa Mental
        activas = sum(1 for e in exps if sum(e) > 0)
        p_total = sum(e[2] for e in exps)
        print(f"[Mapa Mental: {activas} neuronas | Presión Global: {p_total}]")

        # 3. Proyección de Interés (¿Qué le llamó la atención?)
        que_piensa_bella()

        # 4. Grito de Alivio (Respuesta por presión)
        respuesta = evocar()
        print(f"\n>>> Bella dice: {respuesta}")
        # 5. Mecanismo de Consuelo (Equilibrio de bits)
        mecanismo_de_consuelo()
