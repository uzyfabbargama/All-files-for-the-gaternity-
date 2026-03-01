import re
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
nombre_del_archivo = "inventoryclean.N" # Usa el nombre de tu archivo de ejemplo
codigo_n_fuente = leer_codigo_n(nombre_del_archivo)
#guardar (\\) para evitar problemas
# Ahora, la variable 'codigo_n_fuente' contiene todo el texto para tu Parser/Lexer: 
if "Error" not in codigo_n_fuente:
    print(f"--- Archivo '{nombre_del_archivo}' cargado exitosamente ---")
    print(codigo_n_fuente)        
def limpiar_y_extraer_variable(codigo_fuente: str) -> str:
    """
    Busca la primera línea de asignación de código (que contenga '=') 
    y extrae el nombre de la variable principal a la izquierda del signo.
    Ignora las líneas que son comentarios (#).
    """
    
    lineas = codigo_fuente.split('\n')
    
    for linea in lineas:
        # 1. Limpieza de Comentarios y Espacios:
        # Ignora líneas completamente vacías o que son solo comentarios
        linea_limpia = linea.strip()
        if not linea_limpia or linea_limpia.startswith('#'):
            continue
        
        # 2. Búsqueda del Operador de Asignación:
        # Buscamos el signo de asignación de variable principal
        if '=' in linea_limpia:
            # Dividimos la línea en el primer '='
            partes = linea_limpia.split('=', 1)
            # La primera parte es el nombre de la variable (puede tener espacios)
            nombre_variable = partes[0].strip()
            
            # Devolvemos el nombre de la variable y terminamos la función
            return nombre_variable
            
    # Si no se encuentra ninguna asignación, devolvemos un mensaje de error
    return "ERROR: No se encontró una Variable Principal (signo '=') en el código."

# --- EJEMPLO DE USO ---

# Usaremos un bloque de código basado en tu 'inventory.N'
codigo_n_ejemplo = """
#Mi lenguaje N
inventario = (espacio(100,"espacio lleno"),
peso(1),
);
#esto es un comentario
control_peso = {0, peso() += total, stock += 1}
"""


# Extraemos la variable:
variable_principal = limpiar_y_extraer_variable(codigo_n_fuente)

print(f"El código fuente se cargó.")
print(f"La primera Variable Principal detectada es: **{variable_principal}**")

def extraer_subvariables_y_umbrales(codigo_fuente: str, nombre_variable_principal: str) -> list:
    """
    Busca la definición de la variable principal y extrae todas las subvariables y sus parámetros.
    """
    
    # 1. Encontrar la Definición Completa de la Variable Principal
    # Buscamos: 'inventario = (... contenido ...);'
    # NOTA: Usamos 's' flag para que '.' incluya saltos de línea
    patron_principal = re.compile(rf'{nombre_variable_principal}\s*=\s*\((.*?)\);', re.DOTALL)
    
    match = patron_principal.search(codigo_fuente)
    
    if not match:
        print(f"ERROR: No se pudo encontrar el bloque de definición para '{nombre_variable_principal}'.")
        return []
    
    # Contenido: 'espacio(100,"espacio lleno"),\npeso(1),'
    contenido_definicion = match.group(1).strip()
    
    # 2. Patrón de Subvariables: nombre(parámetros)
    # (\w+): Captura el nombre de la variable (letras, números, guiones bajos)
    # \( (.*?) \): Captura el contenido entre paréntesis (parámetros/umbral)
    patron_subvariable = re.compile(r'(\w+)\s*\((.*?)\)', re.DOTALL)
    
    resultados = []
    
    # 3. Iterar y Asignar ID CPC (a partir del ID local 2, ya que 1 es la Clase)
    id_local_contador = 2 
    id_clase_principal = 1
    
    for sub_match in patron_subvariable.finditer(contenido_definicion):
        nombre = sub_match.group(1)
        parametros = sub_match.group(2).strip()
        
        # Asignación de la ID CPC: Concatenar 1 (Clase) + ID Local
        id_cpc = int(f"{id_clase_principal}{id_local_contador}")
        
        resultados.append({
            "nombre": nombre,
            "id_cpc": id_cpc,
            "id_local": id_local_contador,
            "umbral_parametros": parametros
        })
        
        id_local_contador += 1
        
    return resultados

# --- EJEMPLO DE CÓDIGO FUENTE ---

codigo_n_ejemplo = """
# Mi inventario
inventario = (
    espacio(100,"espacio lleno"),
    peso(1),
);
# Definición de otra clase
objetos = (
    total(espacio),
    palo(1)
);
"""

# 1. Definimos la variable principal (que sabemos que es 'inventario')
variable_principal = variable_principal 

# 2. Ejecutamos la extracción de subvariables:
tabla_subvariables = extraer_subvariables_y_umbrales(codigo_n_ejemplo, variable_principal)

# 3. Imprimimos el resultado (La tabla de IDs):
print(f"--- Análisis Léxico de Subvariables para '{variable_principal}' (ID de Clase {1}) ---")
for var in tabla_subvariables:
    print(f"Nombre: {var['nombre']:<10} | ID Local: {var['id_local']} | ID CPC: {var['id_cpc']:<3} | Umbral: {var['umbral_parametros']}")