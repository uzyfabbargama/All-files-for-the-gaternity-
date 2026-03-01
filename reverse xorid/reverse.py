import math

def decodificador_automatico_uziel(id_neurona, char_objetivo):
    # --- LA NUEVA CONSTANTE UZIEL ---
    MAESTRO_LSB = 6 
    
    print(f"\n--- ANALIZANDO ID: {id_neurona} ---")
    
    # 1. Tu nueva ruta: División directa por el LSB Maestro
    # (Ya no buscamos un factor externo, el ID se divide por su propia 'llave')
    resultado_previo = id_neurona / MAESTRO_LSB
    
    # 2. Tu Regla de Oro de Redondeo
    decimal = resultado_previo - int(resultado_previo)
    
    if decimal < 0.5:
        # Si es bajo (como el .33 de 590/6), restamos 1 para compensar el SHL
        resultado_final = int(resultado_previo) - 1
    else:
        # Si es alto, lo dejamos en el entero
        resultado_final = int(resultado_previo)
        
    letra_recuperada = chr(resultado_final)
    error = abs(ord(char_objetivo) - resultado_final)
    
    print(f"Cálculo: {id_neurona} / {MAESTRO_LSB} = {resultado_previo:.4f}")
    print(f"Decimal detectado: {decimal:.4f} -> {'Restando 1' if decimal < 0.5 else 'Manteniendo entero'}")
    print(f"Letra Original: '{char_objetivo}' | Recuperada: '{letra_recuperada}'")
    print(f"Márgen de Error: {error}")
    
    return error == 0

# --- PRUEBA DE CAMPO ---
objetivos = [
    (590, 'a'), # aaa
    (604, 'b'), # bbb (este le erraste)
    (594, 'c')  # ccc (sorprendentemente, este le dijiste bien)
]

# NOTA: Usaré los IDs que generó tu script xorid_dic.py para ser exactos
print("Iniciando escaneo de resonancia...")
exitos = 0

# Prueba con tus IDs reales de la terminal:
# aaa -> 590
# bbb -> ?? (Córrelo en tu PC para ver el ID real de bbb y ccc)
# ccc -> ?? 

# Por ahora probemos el 590 que ya confirmamos:
if decodificador_automatico_uziel(590, 'a'):
    exitos += 1
if decodificador_automatico_uziel(604, 'a'):
    exitos += 1
if decodificador_automatico_uziel(594, 'a'):
    exitos += 1
print(f"\nSincronía lograda en {exitos}/{len(objetivos)} neuronas.")
