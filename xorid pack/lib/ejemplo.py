from xip import XIP
import time
import os

# 1. Inicializar la "Mente"
motor = XIP(buffer_size_mb=4) 
nombre = input("Nombre: ")
def cargar_desde_archivo_xip(ruta):
    if not os.path.exists(ruta):
        print("Archivo no encontrado.")
        return
    
    with open(ruta, "r") as f:
        # Leemos el bloque de texto plano
        raw_data = f.read()
    
    print(f"--- PROCESANDO {len(raw_data)} BYTES DE TEXTO ---")
    
    start = time.time()
    # Aquí ocurre la magia: El Assembler recibe el texto, 
    # busca los delimitadores :: y ,, a velocidad de CPU 
    # y los inyecta en la memoria RAM alineada.
    motor.inyectar(raw_data)
    end = time.time()
    
    print(f"Inyección completada en: {end - start:.6f} seg.")

def guardar_a_texto_xip(ruta):
    start = time.time()
    # Generamos el volcado de texto
    # motor.dump() debería devolver el string formateado variable::valor,,
    # Si no lo tienes, lo reconstruimos desde el diccionario del motor
    with open(ruta, "w") as f:
        for key, value in motor.items():
            f.write(f"{key}:: {value},,\n")
    end = time.time()
    print(f"Exportación a texto lista en: {end - start:.6f} seg.")

# --- TEST DE USO GENERAL ---

# Supongamos que tienes un archivo 'universo.xip' con: estrella1::500,,planeta2::120,,
cargar_desde_archivo_xip(nombre +".xip")

print(f"""
Dato recuperado: 
player: {motor['player']}
level: {motor['level']}
slot1: {motor['slot1']}
slot2: {motor['slot2']}
slot3: {motor['slot3']}
slot4: {motor['slot4']}
""")

