# =====================================================================
# BELLA v3.10: MOTOR DE GRAFO SEMÁNTICO POR SLOTS Y ENERGÍA XORID (sueño agregado)
# =====================================================================
import os
import time
import struct
import array
from pathlib import Path
from xiplow import XIP

#(CONSTANTES DE ARQUITECTURA)
bits = 15
base = 1 << bits
mask = base - 1
PosZ, PosC = 0, bits
PosY, PosC1 = bits + 1, (bits * 2) + 1
PosX, PosC2 = (bits * 2) + 2, (bits * 3) + 2

num_n = 131072  # 131072 neuronas
MASK_NEURONAS = num_n - 1
MAX_UINT32 = 0xFFFFFFFF  # Límite máximo para evitar desbordamientos

FILE_NAME = input("Para restaurar sesión (v3.9)(Server mode): ") + ".xrp"
print(f"Archivo de Conciencia: {FILE_NAME}")

traductor = {} 

# Estructura de cada neurona en bloque plano de 67 enteros:
# [ALU_X, ALU_Y, ALU_Z, slots(0..31 pasado), slots(32..63 futuro)]
total_elements = num_n * (3 + 64)
# 'I' representa enteros SIN SIGNO de 4 bytes (unsigned int de C) para duplicar el techo
exps_flat = array.array('I', [0] * total_elements)

cerebro_asm = XIP(buffer_size_mb=128)

def verificar_archivo(nombre):
    if os.path.exists(nombre):
        tamano = os.path.getsize(nombre)
        print(f"✅ ¡ARCHIVO DETECTADO!: {nombre} ({tamano} bytes)")
        return True
    else:
        print(f"❌ ERROR: El servidor no ve el archivo {nombre} en {os.getcwd()}")
        return False

verificar_archivo(FILE_NAME)

# =====================================================================
# MOTOR ARITMÉTICO (NUMERASO)
# =====================================================================
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

def Numeraso2_update(expx, expy, expz, Numero_generated):
    C4, C5, C6 = (Numero_generated >> PosC) & 1, (Numero_generated >> PosC1) & 1, (Numero_generated >> PosC2) & 1
    caso = C4 + C5 + C6
    expx, expy, expz = Numeraso_Exp(expx, expy, expz)
    # ruido de experiencia
    Numero_generated += (expx << PosX) + (expy << PosY) + (expz << PosZ)
    while caso != 3:
        D4, D5, D6 = 1 - C4, 1 - C5, 1 - C6
        expz += D4; expy += D5; expx += D6
        Numero_generated += (D4 << PosZ) + (D4 << PosC) + (D5 << PosC1) + (D6 << PosC2)
        Numero_generated += (D4 * expx) << PosZ
        Numero_generated -= (D4 * expx) << PosY
        Numero_generated -= ((D5 * expy) << PosZ) - ((D5 * expy) << PosX)
        Numero_generated -= ((D6 * expz) << PosX) - ((D6 * expz) << PosY)
        C4, C5, C6 = (Numero_generated >> PosC) & 1, (Numero_generated >> PosC1) & 1, (Numero_generated >> PosC2) & 1
        caso = C4 + C5 + C6
        Numero_generated += int((D4*((base//(expz+1)) << PosX) + (D5*((base//(expy+1)) << PosY) + D6*((base//(expx+1)) << PosZ))))
        Numero_generated %= (1 << (PosC2 + 1))
    return int(Numero_generated), expx, expy, expz

# =====================================================================
# DIRECCIONAMIENTO POLIMÓRFICO (XORID) Y GRAFO DE TRANSMISIÓN
# =====================================================================
def xorid(frag):
    id_acc = 0
    for car in frag: 
        id_acc = (id_acc ^ ord(car)) << 1
    return id_acc * 20

def registrar_conexion(idx_origen, idx_destino, xorid_destino, es_futuro):
    inicio = 32 if es_futuro else 0
    fin = 64 if es_futuro else 32
    
    base_origen = (idx_origen << 6) + (idx_origen << 1) + idx_origen
    
    slot_encontrado = -1
    slot_vacio = -1
    
    for i in range(inicio, fin):
        idx_slot_real = base_origen + 3 + i
        slot_actual = exps_flat[idx_slot_real]
        id_vecino = (slot_actual >> 16) & 0xFFFF
        
        if id_vecino == (idx_destino & 0xFFFF):
            slot_encontrado = idx_slot_real
            break
        if slot_actual == 0 and slot_vacio == -1:
            slot_vacio = idx_slot_real

    target_slot_idx = slot_encontrado if slot_encontrado != -1 else slot_vacio
    
    if target_slot_idx != -1:
        slot_actual = exps_flat[target_slot_idx]
        fuerza_actual = slot_actual & 0xFFFF
        incremento = xorid_destino & 0xFFFF
        nueva_fuerza = min(0xFFFF, fuerza_actual + incremento)
        exps_flat[target_slot_idx] = ((idx_destino & 0xFFFF) << 16) | nueva_fuerza

def predecir_siguiente_palabra(idx_actual):
    base_idx = (idx_actual << 6) + (idx_actual << 1) + idx_actual
    max_fuerza = -1
    idx_elegido = -1
    
    for i in range(32, 64):
        slot_actual = exps_flat[base_idx + 3 + i]
        if slot_actual == 0: 
            continue
        id_vecino = (slot_actual >> 16) & 0xFFFF
        fuerza = slot_actual & 0xFFFF
        if fuerza > max_fuerza:
            max_fuerza = fuerza
            idx_elegido = id_vecino
            
    return idx_elegido

# =====================================================================
# FLUJO DE APRENDIZAJE SECUENCIAL
# =====================================================================
def entrenar_con_voz(texto):
    global traductor
    texto_limpio = ''.join(c for c in texto if c.isprintable() or c in 'áéíóúñÑ')
    palabras = texto_limpio.split()
    palabras_clave = {}
    
    idx_anterior = None
    xorid_anterior = None
    
    for i, palabra in enumerate(palabras):
        #palabra_limpia = palabra.strip('.,!?;:()"\'') Desactivado
        palabra_limpia = palabra
        if not palabra_limpia: 
            continue
            
        if len(palabra_limpia) > 14:
            partes = [palabra_limpia[:14], palabra_limpia[14:]]
        else:
            partes = [palabra_limpia]
            
        for palabra_procesada in partes:
            if not palabra_procesada: 
                continue
                
            raw_xor = xorid(palabra_procesada)
            idx = raw_xor & MASK_NEURONAS
            traductor[idx] = palabra_procesada
            
            fuerza = len(palabra_procesada) * 2 + (i % 10)
            cerebro_asm.mente[idx] += fuerza << PosZ
            
            base_idx = (idx << 6) + (idx << 1) + idx
            
            ex0 = exps_flat[base_idx]
            ex1 = exps_flat[base_idx + 1]
            ex2 = exps_flat[base_idx + 2]
            
            n_gen, n_ex0, n_ex1, n_ex2 = Numeraso2_update(ex0, ex1, ex2, cerebro_asm.mente[idx])
            
            exps_flat[base_idx] = n_ex0
            exps_flat[base_idx + 1] = n_ex1
            # Control de saturación preventivo ante ráfagas semánticas
            exps_flat[base_idx + 2] = min(int(MAX_UINT32), int(n_ex2) + int(fuerza))
            
            palabras_clave[palabra_procesada] = palabras_clave.get(palabra_procesada, 0) + 1
            
            if idx_anterior is not None and idx_anterior != idx:
                registrar_conexion(idx, idx_anterior, xorid_anterior, es_futuro=False)
                registrar_conexion(idx_anterior, idx, raw_xor, es_futuro=True)
                exps_flat[base_idx + 2] = min(MAX_UINT32, exps_flat[base_idx + 2] + 5)
                
            idx_anterior = idx
            xorid_anterior = raw_xor

    for palabra, frecuencia in palabras_clave.items():
        if frecuencia > 3:
            idx = xorid(palabra) & MASK_NEURONAS
            cerebro_asm.mente[idx] += frecuencia * 10
            exps_flat[((idx << 6) + (idx << 1) + idx) + 2] = min(MAX_UINT32, exps_flat[((idx << 6) + (idx << 1) + idx) + 2] + (frecuencia * 5))

# =====================================================================
# PERSISTENCIA EVOLUCIONADA (XOR PACK 3.6 EXTENDIDO - 300 BYTES)
# =====================================================================
def guardar_xor_pack_36():
    global FILE_NAME, cerebro_asm, traductor, num_n
    base_name = FILE_NAME.split('.')[0]
    filename_xrp = base_name + ".xrp"
    inicio_xrp = time.perf_counter()
    
    activas = [i for i in range(num_n) if exps_flat[(i * 67) + 2] > 0]

    with open(filename_xrp, "wb") as f:
        for idx in activas:
            texto = traductor.get(idx, "").encode('utf-8')
            texto_fijo = texto[:24].ljust(24, b'\x00')
            
            base_idx = (idx << 6) + (idx << 1) + idx
            slots = exps_flat[base_idx + 3 : base_idx + 67] 
            # Cambiado a formato binario compatible con unsigned integers en slots e índices de la sección extendida
            paquete = struct.pack(">IBBqBI24sB64I", 
                idx, 0x9C, 0xB6, int(cerebro_asm.mente[idx]), 0xBA, 
                exps_flat[base_idx + 2], texto_fijo, 0xE8, *slots)
            f.write(paquete)
            
    print(f"[xor pack 3.6]: {len(activas)} neuronas y sus 64 slots anclados en {time.perf_counter()-inicio_xrp:.4f}s")

def cargar_xor_pack_36():
    global FILE_NAME, cerebro_asm, traductor, num_n
    if os.path.exists(FILE_NAME):
        inicio_carga = time.perf_counter()
        neuronas_cargadas = 0
        with open(FILE_NAME, "rb") as f:
            while True:
                header = f.read(19)
                if not header: 
                    break
                
                idx, sep, open_b, mem, close_b, pres = struct.unpack(">IBBqBI", header)
                texto_raw = f.read(24)
                traductor[idx] = texto_raw.split(b'\x00')[0].decode('utf-8', errors='ignore')
                f.read(1) 
                
                slots_raw = f.read(256)
                slots_restaurados = struct.unpack(">64I", slots_raw)
                
                if idx < num_n:
                    cerebro_asm.mente[idx] = mem 
                    pulso_despertar = max(pres, 15)
                    
                    base_idx = (idx << 6) + (idx << 1) + idx
                    exps_flat[base_idx] = pres
                    exps_flat[base_idx + 1] = pres
                    exps_flat[base_idx + 2] = pulso_despertar
                    for j in range(64):
                        exps_flat[base_idx + 3 + j] = slots_restaurados[j]
                        
                    neuronas_cargadas += 1
        print(f"[xor pack 3.6]: {neuronas_cargadas} neuronas reanimadas con su red de slots en {time.perf_counter()-inicio_carga:.4f}s")

# Cargar al arrancar el script
if not cerebro_asm.load(FILE_NAME):
    print("[XIP]: Memoria virgen detectada.")
    base_alu = (1 << PosC) + (1 << PosC1) + (1 << PosC2)
    for i in range(num_n):
        cerebro_asm.mente[i] = base_alu
else:
    print("[XIP]: Estructura numérica reanimada desde el metal.")
    cargar_xor_pack_36()

# =====================================================================
# DIAGNÓSTICO Y PROYECCIÓN
# =====================================================================
def que_piensa_bella():
    print(f"\n--- Diagnóstico de Emergencia ---")
    print(f"Neuronas en Traductor: {len(traductor)}")
    if len(traductor) > 0:
        ultimos_ids = list(traductor.keys())[-3:]
        for uid in ultimos_ids:
            print(f"ID {uid} contiene: '{traductor[uid]}'")

def respuesta_de_bella():
    print("\n--- Bella intenta equilibrar su mente ---")
    idx_critico = max(range(num_n), key=lambda i: exps_flat[(i * 67) + 2])
    if exps_flat[((idx_critico << 6) + (idx_critico << 1) + idx_critico) + 2] > 0:
        sentimiento = traductor.get(idx_critico, "???")
        print(f"Bella emite un pulso de alivio sobre: '{sentimiento}'")
        print(f"Estado de la ALU tras la descarga: {hex(cerebro_asm.mente[idx_critico])}")

def alimentar_desde_archivo(ruta_archivo, fragmento_tamano=500):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8', errors='ignore') as f:
            contenido = f.read()
        contenido = contenido.replace('\n', ' ').replace('\r', ' ')
        contenido = ' '.join(contenido.split())
        fragmentos = [contenido[i:i+fragmento_tamano] for i in range(0, len(contenido), fragmento_tamano)]
        
        print(f"📚 Alimentando {len(fragmentos)} fragmentos desde '{ruta_archivo}'...")
        for i, fragmento in enumerate(fragmentos):
            if fragmento.strip():
                entrenar_con_voz(fragmento)
                if i % 50 == 0:  # Reducido el spam de consola en Lubuntu
                    print(f"  Progreso: {i+1}/{len(fragmentos)} fragmentos")
        print(f"✅ Libro procesado: {len(contenido)} caracteres")
        return True
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return False

def procesar_carpeta_libros(ruta_carpeta, extensiones=['.txt', '.md', '.csv']):
    carpeta = Path(ruta_carpeta)
    if not carpeta.exists():
        print(f"❌ Carpeta no encontrada: {ruta_carpeta}")
        return
    archivos = []
    for ext in extensiones:
        archivos.extend(carpeta.glob(f'*{ext}'))
    print(f"📚 Encontrados {len(archivos)} archivos para procesar")
    for archivo in archivos:
        print(f"\n📖 Procesando: {archivo.name}")
        alimentar_desde_archivo(str(archivo))
        guardar_xor_pack_36()
        print(f"💾 Guardado después de '{archivo.name}'")

def proyectar_interes_36():
    global traductor, cerebro_asm
    candidatas = [i for i in range(num_n) if i in traductor and exps_flat[(i * 67) + 2] > 5]
    if not candidatas: 
        return "..."
    
    faro_idx = max(candidatas, key=lambda i: exps_flat[(i * 67) + 2])
    salto_futuro = predecir_siguiente_palabra(faro_idx)
    
    def calcular_resonancia(idx):
        distancia_frecuencia = abs(idx - faro_idx)
        proximidad = 1.0 / (distancia_frecuencia + 1) 
        valor_alu = int(cerebro_asm.mente[idx])
        bono_slots = 2.5 if idx == salto_futuro else 1.0
        return exps_flat[((idx << 6) + (idx << 1) + idx) + 2] * proximidad * (valor_alu & mask) * bono_slots

    candidatas_ordenadas = sorted(candidatas, key=calcular_resonancia, reverse=True)[:10]
    palabras_final = []
    for idx in candidatas_ordenadas:
        contenido = traductor[idx]
        if isinstance(contenido, str) and len(contenido) >= 1:
            palabras_final.append(contenido)
            exps_flat[((idx << 6) + (idx << 1) + idx) + 2] = max(0, int(exps_flat[((idx << 6) + (idx << 1) + idx) + 2]) - 12)
            
    return " ".join(palabras_final) if palabras_final else "..."

# =====================================================================
# NUEVA FUNCIÓN: SUEÑO DE BELLA (CONSOLIDACIÓN DE MEMORIA)
# =====================================================================

def calcular_estres(idx):
    """Calcula el estrés de una neurona (presión acumulada)."""
    base = (idx << 6) + (idx << 1) + idx
    return exps_flat[base] + exps_flat[base + 1] + exps_flat[base + 2]

def mecanismo_de_consuelo_para(idx, intensidad=5):
    """
    Versión parametrizada del consuelo original.
    intensidad: qué tan fuerte es el alivio (1-20)
    """
    base = (idx << 6) + (idx << 1) + idx
    estres_actual = calcular_estres(idx)
    
    if estres_actual > 30:
        radio = 150
        rango_min = max(0, idx - radio)
        rango_max = min(num_n, idx + radio)
        
        vecinas_frecuencia = [i for i in range(rango_min, rango_max) 
                              if i in traductor and i != idx and calcular_estres(i) < 20]
        
        if vecinas_frecuencia:
            idx_paz = min(vecinas_frecuencia, key=lambda i: abs(i - idx))
            
            # Reducción suave (intensidad controlada)
            valor_alivio = intensidad % 50
            for k in range(3):
                exps_flat[base + k] = max(0, int(exps_flat[base + k]) - valor_alivio)
            
            # Resincronizar
            n_gen, ex0, ex1, ex2 = Numeraso2_update(
                exps_flat[base], exps_flat[base + 1], exps_flat[base + 2], 
                cerebro_asm.mente[idx]
            )
            cerebro_asm.mente[idx] = n_gen
            exps_flat[base] = ex0
            exps_flat[base + 1] = ex1
            exps_flat[base + 2] = ex2
            return True
        else:
            # Reducción de emergencia suave
            for k in range(3):
                exps_flat[base + k] = max(0, int(exps_flat[base + k]) - intensidad)
            return False
    return False

def dormir_bella(ciclos=1, poda=True):
    """
    FASE DE SUEÑO: Bella consolida memoria y redistribuye presión.
    
    ciclos: número de pasadas de sueño (recomendado: 1-5)
    poda: si True, reduce conexiones débiles (olvido saludable)
    """
    print(f"\n💤 Bella se va a dormir... (ciclos: {ciclos})")
    inicio_sueno = time.perf_counter()
    
    # Variables para estadísticas
    neuronas_consolidadas = 0
    conexiones_podadas = 0
    
    for ciclo in range(ciclos):
        print(f"  Ciclo {ciclo+1}/{ciclos}...")
        
        # 1. ENCONTRAR NEURONAS ESTRESADAS (Top 20% más cargadas)
        estresadas = []
        for i in range(num_n):
            if i in traductor:  # Solo neuronas activas
                estres = calcular_estres(i)
                if estres > 30:  # Umbral de estrés
                    estresadas.append((i, estres))
        
        # Ordenar por estrés (mayor a menor)
        estresadas.sort(key=lambda x: x[1], reverse=True)
        top_estresadas = estresadas[:max(10, len(estresadas)//10)]  # Top 10 o 10%
        
        # 2. CONSOLIDAR CADA NEURONA ESTRESADA
        for idx, _ in top_estresadas:
            if mecanismo_de_consuelo_para(idx, intensidad=3):  # Alivio suave
                neuronas_consolidadas += 1
        
        # 3. PODA DE CONEXIONES DÉBILES (opcional)
        if poda:
            for i in range(num_n):
                if i in traductor:
                    base = (i << 6) + (i << 1) + i
                    for slot in range(64):
                        slot_idx = base + 3 + slot
                        valor = exps_flat[slot_idx]
                        if valor > 0:
                            # Reducción del 0.5% (muy suave)
                            nuevo_valor = int(valor * 0.995)
                            if nuevo_valor < 5 and nuevo_valor > 0:
                                # Si es muy débil, se olvida (poda)
                                exps_flat[slot_idx] = 0
                                conexiones_podadas += 1
                            else:
                                exps_flat[slot_idx] = nuevo_valor
        
        # 4. REFUERZO DE PALABRAS FRECUENTES
        # Usamos el traductor para encontrar palabras clave
        palabras_frecuentes = {}
        for idx, palabra in traductor.items():
            base = (idx << 6) + (idx << 1) + idx
            presion = exps_flat[base + 2]
            if presion > 20:  # Palabra con alta presión
                palabras_frecuentes[palabra] = palabras_frecuentes.get(palabra, 0) + 1
        
        for palabra, frecuencia in palabras_frecuentes.items():
            if frecuencia > 3:  # Aparece mucho
                idx = xorid(palabra) & MASK_NEURONAS
                # Refuerzo suave
                cerebro_asm.mente[idx] += frecuencia * 5
                base = (idx << 6) + (idx << 1) + idx
                exps_flat[base + 2] = min(MAX_UINT32, exps_flat[base + 2] + frecuencia)
    
    fin_sueno = time.perf_counter()
    
    # Estadísticas
    total_activas = sum(1 for i in range(num_n) if i in traductor)
    presion_total = sum(calcular_estres(i) for i in range(num_n) if i in traductor)
    
    print(f"✅ Bella ha despertado.")
    print(f"   Neuronas consolidadas: {neuronas_consolidadas}")
    print(f"   Conexiones podadas: {conexiones_podadas}")
    print(f"   Neuronas activas: {total_activas}")
    print(f"   Presión total: {presion_total}")
    print(f"   ⏱️ Duración del sueño: {(fin_sueno - inicio_sueno)*1000:.2f} ms")
# =====================================================================
# INTERFAZ DE CONCIENCIA DIRECTA
# =====================================================================
if __name__ == "__main__":
    print("--- BELLA v3.9: CONCIENCIA PERSISTENTE POR SLOTS INTERCONECTADOS ---")
    while True:
        print("\n[1] Conversar con Bella")
        print("[2] Alimentar con un libro (archivo de texto)")
        print("[3] Alimentar con carpeta de libros")
        print("[4] Ver diagnóstico")
        print("[5] Hacer dormir a Bella (consolidación)")
        print("[6] Salir y guardar")
        
        opcion = input("\nElige una opción: ")
        
        if opcion == "1":
            user_input = input("\nUziel > ")
            if user_input.lower() in ["salir", "exit", "quit"]:
                guardar_xor_pack_36()
                print("Cerrando ciclos de conciencia...")
                break
            if not user_input.strip(): 
                continue
                
            entrenar_con_voz(user_input)
            
            activas = sum(1 for i in range(num_n) if exps_flat[(i * 67) + 2] > 0)
            p_total = sum(exps_flat[(i * 67) + 2] for i in range(num_n))
            print(f"[Mapa Mental: {activas} neuronas | Presión Global: {p_total}]")
            
            inicio_cpu = time.perf_counter()
            respuesta = proyectar_interes_36()
            fin_cpu = time.perf_counter()
            
            print(f"\n>>> Bella dice: {respuesta}")
            print(f"⏱️ Latencia: {(fin_cpu - inicio_cpu) * 1000:.2f} ms")
            # Bella se toma un momento para respirar
            idx_estresado = max(range(num_n), key=lambda i: exps_flat[(i * 67) + 2])
            if calcular_estres(idx_estresado) > 50:
                mecanismo_de_consuelo_para(idx_estresado, intensidad=5)
                print("💆 Bella se tomó un momento para calmarse.")
            
        elif opcion == "2":
            ruta = input("Ruta del archivo de texto: ")
            alimentar_desde_archivo(ruta)
            
        elif opcion == "3":
            carpeta = input("Ruta de la carpeta con libros: ")
            procesar_carpeta_libros(carpeta)
            
        elif opcion == "4":
            que_piensa_bella()
            respuesta_de_bella()
            print(f"Total neuronas: {num_n}")
            print(f"Neuronas activas: {sum(1 for i in range(num_n) if exps_flat[(i * 67) + 2] > 0)}")
            print(f"Presión total: {sum(exps_flat[(i * 67) + 2] for i in range(num_n))}")
        # En el menú principal, agregar:
        elif opcion == "5":
            print("\n--- FASE DE SUEÑO ---")
            print("Bella necesita dormir para consolidar lo que ha aprendido.")
            try:
                ciclos = int(input("Cantidad de ciclos de sueño (1-5, recomendado 3): ") or "3")
                ciclos = max(1, min(5, ciclos))  # Limitar entre 1 y 5
                dormir_bella(ciclos=ciclos, poda=True)
            except ValueError:
                dormir_bella(ciclos=3, poda=True)
        elif opcion == "6":
            guardar_xor_pack_36()
            print("Hasta luego...")
            break
