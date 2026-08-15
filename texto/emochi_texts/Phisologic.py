# -*- coding: utf-8 -*-
import os

# Configuración
CARPETA_INPUT = "./"  # Donde están los archivos de Emochi
CARPETA_OUTPUT = "./limpios"

if not os.path.exists(CARPETA_OUTPUT):
    os.makedirs(CARPETA_OUTPUT)

def limpiar_entrada_emochi(texto_sucio):
    # Reemplazamos saltos de línea por espacios para mantener la continuidad del "fluido"
    # y eliminamos espacios dobles que puedan quedar
    limpio = texto_sucio.replace("\n", " ").strip()
    while "  " in limpio: # Limpieza de dobles espacios para optimizar bits
        limpio = limpio.replace("  ", " ")
    return limpio

def convertir_archivo(nombre_archivo):
    ruta_entrada = os.path.join(CARPETA_INPUT, nombre_archivo)
    # Generamos el nombre de salida cambiando la extensión a .txt
    nombre_salida = os.path.splitext(nombre_archivo)[0] + ".txt"
    ruta_salida = os.path.join(CARPETA_OUTPUT, nombre_salida)

    try:
        with open(ruta_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        texto_final = limpiar_entrada_emochi(contenido)

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(texto_final)
        
        print(f"✔ Procesado: {nombre_archivo} -> {nombre_salida}")
    except Exception as e:
        print(f"✘ Error en {nombre_archivo}: {e}")

# Procesar todo
for archivo in os.listdir(CARPETA_INPUT):
    # Procesa archivos de texto o json (ajusta según lo que descargues de Emochi)
    if archivo.endswith(".txt") or archivo.endswith(".json"):
        if archivo != "manifest.json" and "limpiar" not in archivo:
            convertir_archivo(archivo)

print(f"\n🚀 Proceso terminado. El fluido BHL está listo en: {CARPETA_OUTPUT}")
