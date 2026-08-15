# =====================================================================
# EXTRACTOR LINEAL JAVACRAFT - GENERADOR DE .EQU NATIVO (1.12.2)
# =====================================================================
import csv

# 1. Cargamos los métodos estáticos en un set para búsquedas instantáneas O(1)
metodos_estaticos = set()
try:
    with open("STATIC_METHODS.txt", "r") as f:
        for linea in f:
            linea_limpia = linea.strip()
            if linea_limpia:
                metodos_estaticos.add(linea_limpia)
    print(f"[+] {len(metodos_estaticos)} métodos estáticos cargados.")
except FileNotFoundError:
    print("[!] STATIC_METHODS.txt no encontrado. Se asumirán métodos de instancia.")

# 2. Mapeamos los identificadores humanos desde los CSVs
mapa_nombres = {} # func_ o field_ -> nombre humano

# Parseamos métodos
with open("methods.csv", mode="r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        mapa_nombres[fila["searge"]] = fila["name"]

# Parseamos campos
with open("fields.csv", mode="r", encoding="utf-8") as f:
    lector = csv.DictReader(f)
    for fila in lector:
        mapa_nombres[fila["searge"]] = fila["name"]

print(f"[+] {len(mapa_nombres)} traducciones humanas indexadas en memoria.")

# 3. Procesamos el joined.srg para encontrar el binario real de Mojang
# Queremos traducir: Nombre Humano -> Código Ofuscado Real
macros_generadas = []

macros_generadas.append("# =====================================================================")
macros_generadas.append("# EQUIVALENCIAS NATIVAS AUTOMÁTICAS PARA MINECRAFT 1.12.2 (RAW EQU)")
macros_generadas.append("# Generado por la suite Javacraft")
macros_generadas.append("# =====================================================================\n")

with open("joined.srg", "r") as f_srg:
    for linea in f_srg:
        partes = linea.strip().split()
        if not partes:
            continue
        
        # Procesamos los métodos (MD:)
        if partes[0] == "MD:":
            # Estructura SRG: MD: clase/ofuscado descriptor clase_mcp/func_ descriptor_mcp
            ofuscado_mojang = partes[1].split("/")[-1]
            intermedio_mcp = partes[3].split("/")[-1]
            clase_destino = partes[3].replace("/", ".") # Formato paquete Java
            clase_destino_limpia = clase_destino.split(".func_")[0]
            
            if intermedio_mcp in mapa_nombres:
                nombre_humano = mapa_nombres[intermedio_mcp]
                macro_macro = f"MC_{nombre_humano.upper()}"
                
                # Si es estático, se llama con la Clase. Si no, asumimos que se le pasa el objeto 'usr'
                if intermedio_mcp in metodos_estaticos:
                    linea_equ = f"{macro_macro}(args) :: {clase_destino_limpia}.{ofuscado_mojang}(args)"
                else:
                    linea_equ = f"{macro_macro}(usr, args) :: usr.{ofuscado_mojang}(args)"
                macros_generadas.append(linea_equ)

        # Procesamos los campos (FD:)
        elif partes[0] == "FD:":
            ofuscado_mojang = partes[1].split("/")[-1]
            intermedio_mcp = partes[2].split("/")[-1]
            
            if intermedio_mcp in mapa_nombres:
                nombre_humano = mapa_nombres[intermedio_mcp]
                macro_macro = f"FIELD_{nombre_humano.upper()}"
                linea_equ = f"{macro_macro}(usr) :: usr.{ofuscado_mojang}"
                macros_generadas.append(linea_equ)

# 4. Escupimos el archivo .equ final de alto rendimiento
with open("mcp_nativo_1.12.2.equ", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(macros_generadas))

print("\n[+] ¡ÉXITO ABSOLUTO!")
print("Archivo 'mcp_nativo_1.12.2.equ' generado y listo para Javacraft.")
