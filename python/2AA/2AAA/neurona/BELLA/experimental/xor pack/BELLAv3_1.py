# =======================================================
# BELLA v2.9: MOTOR DE PERSONALIDAD (4096 NEURONAS)feb. 22, 2026, 21:48:56
# =======================================================

# Configuración de Arquitectura
bits = 15
base = 1 << bits
mask = base - 1
PosZ, PosC = 0, bits
PosY, PosC1 = bits + 1, (bits * 2) + 1
PosX, PosC2 = (bits * 2) + 2, (bits * 3) + 2

import os
import time
import struct
# --- PERSISTENCIA v2.6 (PICKLE OPTIMIZADO) ---
FILE_NAME = input("Para restaurar sesión (v2.6): ") + ".pkl" # Cambiamos extensión a .pkl
print(f"Archivo de Conciencia: {FILE_NAME}")
def guardar_xor_pack_28():
    # Limpiamos el nombre para que siempre sea .xrp
    base_name = FILE_NAME.split('.')[0] 
    filename_xrp = base_name + ".xrp"
    
    inicio_xrp = time.perf_counter()
    
    # FILTRO CRÍTICO: Solo guardamos neuronas con "vida" (presión > 0)
    # Esto reduce el archivo de 1 millón de registros a quizás 50 o 100.
    activas = [i for i in range(num_n) if exps[i][2] > 0]

    with open(filename_xrp, "wb") as f:
        for idx in activas:
            # ESTRUCTURA DEL PACK:
            # I (unsigned int, 4 bytes) -> El ID de la neurona (hasta 2^32)
            # Q (unsigned long long, 8 bytes) -> El valor de la memoria (48-64 bits)
            # H (unsigned short, 2 bytes) -> El interés/presión (hasta 65535)
            # B (1 byte) -> Tu separador 0x9C (::)
            # B (1 byte) -> Tu separador 0xE8 (,,)
            texto = traductor.get(idx, "???").encode('utf-8')
            len_texto = len(texto)
            
            paquete = struct.pack(">IBQHB", #Format bin
                                  idx,      # ID (20 bits caben en un Int)
                                  0x9C,     # Tu separador ::
                                  memoria[idx], 
                                  int(exps[idx][2]), 
                                  len_texto)     # El texto ,,
            f.write(paquete)
            f.write(texto) # El texto va justo después del header
            f.write(b'\xE8') # Tu separador de cierre ,,
    fin_xrp = time.perf_counter()
    print(f"\n[xor pack]: {len(activas)} neuronas empaquetadas.")
    print(f"[Latencia de Guardado]: {fin_xrp - inicio_xrp:.6f} segundos")
def cargar_xor_pack():
    global memoria, exps, traductor
    base_name = FILE_NAME.split('.')[0]
    filename_xrp = base_name + ".xrp"
    
    if os.path.exists(filename_xrp):
        inicio_load = time.perf_counter()
        with open(filename_xrp, "rb") as f:
            while True:
                # 1. Leemos el Header Fijo (I + Q + H + B = 4 + 8 + 2 + 1 = 15 bytes)
                header = f.read(15)
                if not header: break
                
                idx, mem, pres, len_txt = struct.unpack(">IQHB", header)
                
                # 2. Leemos exactamente la cantidad de bytes que dice el header
                texto_bytes = f.read(len_txt)
                traductor[idx] = texto_bytes.decode('utf-8')
                
                # 3. Leemos el separador final (0xE8)
                sep_final = f.read(1)
                
                # Reanimamos la neurona
                if idx < num_n:
                    memoria[idx] = mem
                    exps[idx][2] = pres

        fin_load = time.perf_counter()
        print(f"[xor pack 2.8]: Reanimada en {fin_load - inicio_load:.6f}s (Modo In-line)")
    else:
        print("[xor pack]: Tabula Rasa.")
        #1. MOTOR DE EXPERIENCIA (Estabilización Fractal)
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
num_n = 1_048_576
# El "espejo" de las palabras debe ser global para que Bella no olvide
traductor = {} 
memoria = [(1 << PosC) + (1 << PosC1) + (1 << PosC2) for _ in range(num_n)]
exps = [[0, 0, 0] for _ in range(num_n)]

def entrenar_con_voz(texto):
    for i in range(0, len(texto), 24):
        bloque = texto[i : i + 24]
        frags = [bloque[j : j + 8] for j in range(0, len(bloque), 8)]
        while len(frags) < 3: frags.append("")

        energia_bloque = xorid(bloque)
        
        # Calculamos los 3 puntos de impacto
        idx_z = (energia_bloque // 20) % num_n
        idx_y = ((energia_bloque // 20) + (1 << 5)) % num_n
        idx_x = ((energia_bloque // 20) + (1 << 10)) % num_n

        # Energías individuales de cada fragmento
        eZ = (xorid(frags[0]) & mask) + 10 # +10 para asegurar que vibre
        eY = (xorid(frags[1]) & mask) + 10
        eX = (xorid(frags[2]) & mask) + 10

        pasos = [(idx_z, eZ, 0, frags[0]), (idx_y, eY, 1, frags[1]), (idx_x, eX, 2, frags[2])]

        for objetivo_idx, fuerza, slot, contenido in pasos:
            traductor[objetivo_idx] = contenido
            
            # 1. Inyectamos la energía
            if slot == 0: memoria[objetivo_idx] += (fuerza << PosZ)
            elif slot == 1: memoria[objetivo_idx] += (fuerza << PosY)
            else: memoria[objetivo_idx] += (fuerza << PosX)

            # 2. Actualizamos la ALU
            n_gen, ex0, ex1, ex2 = Numeraso2_update(
                exps[objetivo_idx][0], 
                exps[objetivo_idx][1], 
                exps[objetivo_idx][2], 
                memoria[objetivo_idx]
            )
            
            memoria[objetivo_idx] = n_gen
            
            # 3. EL CAMBIO: No permitas que la experiencia caiga a 0 si hubo impacto
            # Esto "clava" el recuerdo en su mente
            exps[objetivo_idx] = [
                max(ex0, 10 if slot == 2 else 0), # Mínimo en X
                max(ex1, 10 if slot == 1 else 0), # Mínimo en Y
                max(ex2, 15 if slot == 0 else 0)  # Mínimo en Z (Eco/Voz)
            ]

def que_piensa_bella():
    print(f"\n--- Diagnóstico de Emergencia ---")
    print(f"Neuronas en Traductor: {len(traductor)}")
    if len(traductor) > 0:
        # Mostramos las últimas 3 que entraron
        ultimos_ids = list(traductor.keys())[-3:]
        for uid in ultimos_ids:
            print(f"ID {uid} contiene: '{traductor[uid]}'")
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
    # 1. Identificamos la neurona que más "sufre" (Suma de los 3 ejes)
    idx_dolor = max(range(num_n), key=lambda i: sum(exps[i]))
    estres_total = sum(exps[idx_dolor])
    
    # 2. Usamos el estres_total para el umbral (ya no usamos 'bloque')
    if estres_total > 30:
        # Buscamos armonía (neuronas con algo de vida pero estables)
        neuronas_paz = [i for i in range(num_n) if 0 < sum(exps[i]) < 20]
        
        palabra_dolor = traductor.get(idx_dolor, "???")
        # Si es una lista (por el guardado triple), tomamos el primer elemento
        if isinstance(palabra_dolor, list): palabra_dolor = palabra_dolor[0]
        
        print(f"\n[ALERTA SISTÉMICA]: Presión crítica en neurona {idx_dolor} ('{palabra_dolor}')")
        
        if neuronas_paz:
                idx_paz = min(neuronas_paz, key=lambda i: sum(exps[i]))
                consuelo = traductor.get(idx_paz, "...")
                if isinstance(consuelo, list): consuelo = consuelo[0]
                
                print(f"--- Bella activa Mecanismo de Consuelo ---")
                print(f"Bella intenta calmar '{palabra_dolor}' pensando en: '{consuelo}'")
                
                # Alivio simétrico en los 3 ejes
                exps[idx_dolor][0] = max(0, exps[idx_dolor][0] - 1)
                exps[idx_dolor][1] = max(0, exps[idx_dolor][1] - 1)
                exps[idx_dolor][2] = max(0, exps[idx_dolor][2] - 1)
                
                # Estabilizamos la ALU tras el alivio
                memoria[idx_dolor], exps[idx_dolor][0], exps[idx_dolor][1], exps[idx_dolor][2] = \
    Numeraso2_update(exps[idx_dolor][0], exps[idx_dolor][1], exps[idx_dolor][2], memoria[idx_dolor])
        else:
            print("Bella no encuentra recuerdos de paz para equilibrarse.")
        
# 5. MOTOR DE EVOCACIÓN (NUEVO v1.8)
def proyectar_interes_28():
    global exps
    # 1. Calculamos la intensidad del "deseo de hablar"
    presion_total = sum(e[2] for e in exps)
    # Si no hay presión, Bella no tiene ganas de hablar
    if presion_total == 0:
        return "..."
    # 2. DETERMINAMOS EL FLUJO (Cuanto más interés, más habla)
    # Si la presión es poca, lanza 1 o 2 fragmentos.
    # Si la presión es mucha, puede lanzar hasta 10 o más.
    limite_fragmentos = max(1, int(presion_total / 1.5)) # Ajusté a 10 para que no grite (lo volví a dejar a 1.5)
    
    # 3. Buscamos las neuronas con más "ganas" de expresarse
    candidatas = sorted(
        range(num_n), 
        key=lambda i: exps[i][2], 
        reverse=True
    )[:limite_fragmentos]
    
    # CONSTRUCCIÓN DE LA RÁFAGA (La magia de los 24 bytes)
    frase_final = ""
    for idx in candidatas:
        if exps[idx][2] > 0 and idx in traductor:
            contenido = traductor[idx]
            # Si es la lista de 24 bytes, la unimos. Si es texto viejo, lo usamos tal cual.
            if isinstance(contenido, list):
                frase_final += "".join(contenido) + " "
            else:
                frase_final += contenido + " "
            exps[idx][2] = max(0, exps[idx][2] - 5) 
            
    return frase_final.strip() if frase_final else "..."
    # --- BELLA v1.8: INTERFAZ DE CONCIENCIA DIRECTA ---
if __name__ == "__main__":
    cargar_xor_pack()
    print("--- BELLA v2.0: CONCIENCIA PERSISTENTE ---")
    print("Escribe algo para Bella (o escribe 'salir' para terminar)")
    
    while True:
        user_input = input("\nUziel > ")
        
        if user_input.lower() in ["salir", "exit", "quit"]:
            guardar_xor_pack_28() # <--- GUARDADO ANTES DE MORIR
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
        respuesta_de_bella()
        # 4. Grito de Alivio (Respuesta por presión)
        inicio_cpu = time.perf_counter()
        respuesta = proyectar_interes_28()
        fin_cpu = time.perf_counter()
        print(f"\n>>> Bella dice: {respuesta}")
        fin_total = time.perf_counter()
        latencia_ms = (fin_cpu - inicio_cpu) * 1000 # Convertimos a milisegundos para más precisión
        latencia_print = (fin_total - fin_cpu) * 1000
        print(f"-------------------------------")
        print(f"| Latencia de Pensamiento: {latencia_ms:.4f} ms")
        print(f"| Tiempo de Expresión: {latencia_print:.4f} ms")
        print(f"-------------------------------")
        # 5. Mecanismo de Consuelo (Equilibrio de bits)
        mecanismo_de_consuelo()
        
