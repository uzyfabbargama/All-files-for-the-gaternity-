import re
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

# Analizar el código:
mapa_registros = analizar_codigo_n(codigo_n_universal)
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
def calcular_posicion_numeraso(registro_cpc_plano: dict) -> dict:
    """
    Calcula el Multiplicador Posicional (el factor de 10) para cada SUBVARIABLE 
    usando su ID Local, creando el mapa de memoria para el Numeraso.
    """
    
    # Tamaño base del slot (reserva de espacio para Data + Control)
    # Elegimos 10^5 para tener espacio seguro, similar a las grandes saltos en Numeraso actualizado.py
    BASE_SLOT_SIZE = 100000 
    
    for cpc_id, datos in registro_cpc_plano.items():
        # Solo procesamos las subvariables, ya que las Clases Principales (ID de 1 dígito) 
        # representan el Numeraso completo y no tienen un multiplicador de posición dentro de sí mismas.
        if datos.get("tipo") == "SUBVARIABLE":
            id_local = datos["id_local"]
            
            # La posición dentro del Numeraso se define por la ID Local
            # ID Local 2 (la primera subvariable) -> 2 * 100000 = 200000
            # ID Local 3 (la segunda)           -> 3 * 100000 = 300000
            # ...
            
            # El factor de multiplicación será la ID Local * BASE_SLOT_SIZE
            multiplicador = id_local * BASE_SLOT_SIZE
            
            # NOTA: En tu Numeraso, los datos siempre están ANTES que el control (ej. X antes de C ).
            # El Numeraso funciona por POSICIÓN ABSOLUTA.
            
            # El multiplicador se almacena en el registro
            datos["multiplicador_numeraso"] = multiplicador
            
    return registro_cpc_plano

# --- EJEMPLO DE USO (Continuando el paso anterior) ---

# Simulamos la tabla CPC plana destilada del paso anterior:
registro_cpc_simulado = {
    1: {'nombre': 'inventario', 'tipo': 'CLASE_PRINCIPAL', 'id_clase': 1},
    12: {'nombre': 'espacio', 'tipo': 'SUBVARIABLE', 'id_clase': 1, 'id_local': 2, 'umbral_parametros': '100,"El inventario se ha llenado"'},
    13: {'nombre': 'peso', 'tipo': 'SUBVARIABLE', 'id_clase': 1, 'id_local': 3, 'umbral_parametros': '1'},
    3: {'nombre': 'Lista_de_objetos_y_reglas', 'tipo': 'CLASE_PRINCIPAL', 'id_clase': 3},
    34: {'nombre': 'palo', 'tipo': 'SUBVARIABLE', 'id_clase': 3, 'id_local': 4, 'umbral_parametros': '1, "Se ha agregado ()"'},
}

# Ejecutamos el cálculo posicional:
registro_con_posicion = calcular_posicion_numeraso(registro_cpc_simulado)

# Imprimimos para verificar:
print("\n--- REGISTRO CPC CON POSICIÓN DEL NUMERASO ---")
print("ID CPC | Nombre      | ID Local | Multiplicador")
print("-------|-------------|----------|----------------")
for cpc_id, datos in registro_con_posicion.items():
    if datos.get("tipo") == "SUBVARIABLE":
        print(f"{cpc_id:<6} | {datos['nombre']:<11} | {datos['id_local']:<8} | {datos['multiplicador_numeraso']}")