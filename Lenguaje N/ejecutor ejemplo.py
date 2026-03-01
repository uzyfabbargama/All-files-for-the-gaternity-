import re
import ctypes
# 1. Cargar la librería C (el motor de rendimiento)
runtime_n = ctypes.CDLL('./runtime_n.so') 

# 2. Definir los tipos de datos que se esperan (64 bits)
runtime_n.ejecutar_operacion_densa.argtypes = [ctypes.c_uint64, ctypes.c_uint64, ctypes.c_uint64]
PosZ = ((10)**6)**0
PosY = ((10)**6)**1
PosX = ((10)**6)**2
Archivo = input("Define como se llama tu archivo .N: ")
def leer_codigo_n(nombre_archivo: str) -> str:
    """
    Abre y lee el contenido completo del archivo .N especificado.
    """
    try:
        # 'with open' asegura que el archivo se cierre automáticamente
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo_n:
            # .read() lee todo el contenido del archivo como una sola cadena (string)
            contenido = archivo_n.read()
            return contenido
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{nombre_archivo}'. Asegúrate de que esté en la misma carpeta."

# Uso del lector:
nombre_del_archivo = Archivo + ".N" # Usa el nombre de tu archivo de ejemplo
codigo_n_fuente = leer_codigo_n(nombre_del_archivo)
#guardar (\\) para evitar problemas
# Ahora, la variable 'codigo_n_fuente' contiene todo el texto para tu Parser/Lexer: 
if "Error" not in codigo_n_fuente:
    print(f"--- Archivo '{nombre_del_archivo}' cargado exitosamente ---")
    print(codigo_n_fuente)        

def analizar_codigo_n(codigo_fuente: str) -> dict:
    """
    Escanea todo el código fuente de 'N', identifica Clases y Subvariables,
    y les asigna su ID de Codificación de Posición Concatenada (CPC).

    Retorna un diccionario mapeando 'Clase' -> [Subvariables y sus IDs].
    """
    
    # Expresión Regular para encontrar TODAS las declaraciones de Clases/Variables Principales.
    # Esto busca: Nombre = ContenidoBlock;
    # (\w+)\s*=\s* -> Captura el nombre (Grupo 1) hasta el '='.
    # ([({].*?[)}]);  -> Captura el contenido del bloque completo, ya sea (..); o {..}; (Grupo 2).
    # re.DOTALL es crucial para manejar saltos de línea dentro de los bloques.
    patron_clase_principal = re.compile(r'(\w+)\s*=\s*([({].*?[)}]);', re.DOTALL | re.MULTILINE)
    
    # Expresión Regular para encontrar Subvariables dentro de un bloque de Clase.
    # (\w+)\s*\(     -> Captura el nombre de la subvariable (Grupo 1)
    # (.*?)\)         -> Captura los parámetros/umbral (Grupo 2)
    patron_subvariable = re.compile(r'(\w+)\s*\((.*?)\)', re.DOTALL)
    
    tabla_simbolos = {}
    id_clase_contador = 1  # Inicia en 1 para la primera clase
    
    # 1. ITERAR TODAS LAS CLASES (Variables Principales)
    for match_clase in patron_clase_principal.finditer(codigo_fuente):
        nombre_clase = match_clase.group(1).strip()
        contenido_bloque = match_clase.group(2).strip() # Contiene (..); o {..};
        
        # Ignoramos la sintaxis del control_objeto() = ( ... ) por ahora (la función vacía),
        # pero mantenemos el ID.
        if nombre_clase.endswith("()"):
            nombre_clase = nombre_clase[:-2] # Eliminar '()'
            
        # Almacenar la nueva clase en la tabla de símbolos
        tabla_simbolos[nombre_clase] = {
            "id_clase": id_clase_contador,
            "tipo_bloque": "Data" if contenido_bloque.startswith('(') else "Control",
            "subvariables": []
        }
        
        # 2. PROCESAR SUBVARIABLES DENTRO DEL BLOQUE
        id_local_contador = 2  # Inicia en 2 para la primera propiedad (1 es la clase misma)
        
        # Extraemos el contenido sin los delimitadores externos (e.g., sin el '(', ')' y ';')
        # Esto simplifica la búsqueda de subvariables.
        contenido_interno = contenido_bloque.strip()[1:-2].strip()
        
        for sub_match in patron_subvariable.finditer(contenido_interno):
            nombre_sub = sub_match.group(1)
            parametros = sub_match.group(2).strip()
            
            # 3. ASIGNACIÓN DEL ID CPC (Concatenación)
            # Ejemplo: Clase 1 + Local 2 -> ID 12
            id_cpc = int(f"{id_clase_contador}{id_local_contador}")
            
            tabla_simbolos[nombre_clase]["subvariables"].append({
                "nombre": nombre_sub,
                "id_cpc": id_cpc,
                "id_local": id_local_contador,
                "umbral_parametros": parametros
            })
            
            id_local_contador += 1
            
        id_clase_contador += 1
        
    return tabla_simbolos

# --- CÓDIGO DE PRUEBA UNIVERSAL (Basado en tus snippets) ---

codigo_n_universal = """
# Mi inventario
inventario = (
    espacio(100,"El inventario se ha llenado"),
    peso(1)
); # Fin de la Clase 1

control_peso = {0, stock+=1, total += peso()}; # Clase de Control 2 (no tiene subvariables con ())

Lista_de_objetos_y_reglas = (
    total(espacio),
    control_objeto(1),
    palo(1, "Se ha agregado ()"),
    espada(1)
); # Fin de la Clase 3

experiencia_del_jugador = (
    nivel(100, "has alcanzado el máximo nivel"),
    XP(10, "has subido de nivel")
); # Fin de la Clase 4
"""
# --- NUEVA FUNCIÓN ---
def destilar_registro_cpc(mapa_registros: dict) -> dict:
    """
    Toma el mapa de registros anidado y lo convierte en el registro CPC plano.
    """
    registro_cpc_plano = {} # Diccionario plano: ID_CPC -> {Datos}

    for nombre_clase, datos_clase in mapa_registros.items():
        clase_id = datos_clase['id_clase']
        
        # 1. Registrar la CLASE PRINCIPAL (e.g., ID 1, 2, 3)
        registro_cpc_plano[clase_id] = {
            "nombre": nombre_clase,
            "tipo": "CLASE_PRINCIPAL",
            "id_clase": clase_id
        }
        
        # 2. Registrar las SUBVARIABLES (e.g., ID 12, 34)
        if datos_clase.get('subvariables'): # Usar .get para seguridad
            for sub_var in datos_clase['subvariables']:
                id_cpc = sub_var['id_cpc']
                
                registro_cpc_plano[id_cpc] = {
                    "nombre": sub_var['nombre'],
                    "tipo": "SUBVARIABLE",
                    "id_clase": clase_id,
                    "id_local": sub_var['id_local'],
                    "umbral_parametros": sub_var['umbral_parametros']
                }
                
    return registro_cpc_plano
# Analizar el código:
mapa_registros = analizar_codigo_n(codigo_n_fuente)
# --- NUEVO PASO: DESTILACIÓN DE VARIABLES ---
registro_cpc_plano = {} # Diccionario plano: ID_CPC -> {Datos}

# 1. Iterar sobre el mapa de registros anidado
for nombre_clase, datos_clase in mapa_registros.items():
    clase_id = datos_clase['id_clase']
    
    # El nombre de la Clase Principal también es una 'variable' con ID de 1 dígito (e.g., 1, 2, 3...)
    # Aunque la ID CPC es normalmente de 2 dígitos, guardamos la Clase en sí misma.
    registro_cpc_plano[clase_id] = {
        "nombre": nombre_clase,
        "tipo": "CLASE_PRINCIPAL",
        "id_clase": clase_id
    }
    
    # 2. Iterar sobre las Subvariables (Propiedades)
    if datos_clase['subvariables']:
        for sub_var in datos_clase['subvariables']:
            id_cpc = sub_var['id_cpc']
            
            # Guardamos la Subvariable mapeada directamente a su ID CPC (ej. 12, 34)
            registro_cpc_plano[id_cpc] = {
                "nombre": sub_var['nombre'],
                "tipo": "SUBVARIABLE",
                "id_clase": clase_id,
                "id_local": sub_var['id_local'],
                "umbral_parametros": sub_var['umbral_parametros']
            }

# --- IMPRESIÓN DEL RESULTADO DESTILADO ---
print("\n--- REGISTRO CPC PLANO (Mapa de Memoria del Runtime) ---")
print("ID CPC | Tipo                | Nombre        | Umbral")
print("-------|---------------------|---------------|----------------------")
# Para imprimir ordenado, convertimos las claves (IDs) a enteros y las ordenamos
claves_ordenadas = sorted(registro_cpc_plano.keys()) 

for cpc_id in claves_ordenadas:
    datos = registro_cpc_plano[cpc_id]
    
    # Formateo de la salida
    nombre = datos['nombre']
    tipo = datos['tipo']
    umbral = datos.get('umbral_parametros', '-')
    
    # Imprimimos la variable destilada, lista para el motor
    print(f"{cpc_id:<6} | {tipo:<19} | {nombre:<13} | {umbral}")
try:
    runtime_n = ctypes.CDLL('./runtime_n.so') 
except OSError:
    try:
        runtime_n = ctypes.CDLL('./runtime_n.dll')
    except OSError:
        print("Error: No se encontró la librería compartida 'runtime_n.so' o 'runtime_n.dll'. ¡Compila el C primero!")
        exit()

# 2. Definir los tipos de datos de las funciones de C
UInt64 = ctypes.c_uint64

runtime_n.ejecutar_operacion_densa.argtypes = [UInt64, UInt64, UInt64]
runtime_n.ejecutar_operacion_densa.restype = None # La función no retorna valor, solo modifica la memoria

full_umbral_string = registro_cpc_plano[12]['umbral_parametros']
numero_umbral = full_umbral_string.split(',',1) #Parte a la mitad apartir de la coma
numero_str = numero_umbral[0].strip() #obtiene el número
print (numero_umbral)
valor_numerico = int(numero_str) #lo combierte a entero
valor_numerico *= (PosX)
print(valor_numerico) #ahora que es entero lo imprime
import ctypes

# 1. Cargar la librería C (el motor de rendimiento)
try:
    # Usamos el nombre del archivo compilado exitosamente
    runtime_n = ctypes.CDLL('./runtime_n.so') 
except OSError:
    try:
        runtime_n = ctypes.CDLL('./runtime_n.dll') # Opción para Windows
    except OSError:
        print("Error: No se encontró la librería compartida 'runtime_n.so' o 'runtime_n.dll'.")
        exit()

# 2. Definir los tipos de datos de las funciones de C
UInt64 = ctypes.c_uint64

# Definición de la función central de ejecución
runtime_n.ejecutar_operacion_densa.argtypes = [UInt64, UInt64, UInt64]
runtime_n.ejecutar_operacion_densa.restype = None

# Nuevas funciones para la inicialización y lectura de la memoria
runtime_n.inicializar_memoria.argtypes = [UInt64, UInt64]
runtime_n.inicializar_memoria.restype = None

runtime_n.obtener_estado_cpc.argtypes = [UInt64]
runtime_n.obtener_estado_cpc.restype = UInt64 


# --- BUCLE DE EJECUCIÓN (DEMO DE CARGA Y EJECUCIÓN) ---

print("\n--- INICIALIZACIÓN DEL MOTOR N (C-Runtime) ---")

# IDs del Agente_IA.N (Necesitarías el parser completo para obtenerlos automáticamente)
# Asumimos estos IDs para la demo de la batería agotada (de tu ejemplo previo)
ID_BATERIA = 43  
ID_TOTAL_PROBLEMAS = 10 
CONSUMO_VALOR = 100 

# La IND de control_energía {1, total += "Se ha acabado la energía"}
# Usamos un número codificado grande para simular la IND real generada por el parser:
IND_CONTROL_ENERGIA_LOGICA = 10000000000000000000000000000000

# 1. Inicializar la memoria C con los valores de umbral
# El motor C recibe: ID CPC (43) y Valor Inicial (100)
runtime_n.inicializar_memoria(ID_BATERIA, 100) 
runtime_n.inicializar_memoria(ID_TOTAL_PROBLEMAS, 0) 

print(f"Estado inicial: Batería: {runtime_n.obtener_estado_cpc(ID_BATERIA)}, Total de problemas: {runtime_n.obtener_estado_cpc(ID_TOTAL_PROBLEMAS)}")

# 2. Ejecutar la instrucción crítica: 'Agente += Agente(consumo)*100'
print("\nEJECUTANDO IND: Descontando consumo crítico (100)...")
# Python envía los números directamente a la función C
runtime_n.ejecutar_operacion_densa(
    ID_BATERIA,             # id_bateria
    CONSUMO_VALOR,          # valor_consumo (la operación que genera el acarreo)
    IND_CONTROL_ENERGIA_LOGICA # IND (la lógica a ejecutar si hay acarreo)
)

# 3. Leer el resultado del motor C (El estado post-ejecución)
print("--- RESULTADO DE LA ALU ---")
bateria_final = runtime_n.obtener_estado_cpc(ID_BATERIA)
total_final = runtime_n.obtener_estado_cpc(ID_TOTAL_PROBLEMAS)
print(f"Batería final: {bateria_final}")
print(f"Total de problemas (Acarreo): {total_final}")

# Verificación de la Lógica 'N'
if total_final == 1:
    print("✅ **¡Éxito!** El motor C detectó que el umbral fue cruzado (batería <= 0) y activó la lógica del acarreo (Total += 1).")
else:
    print("❌ Error en la lógica. El acarreo no se activó.")

