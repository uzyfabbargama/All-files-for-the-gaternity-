import re

def analizar_codigo_n(codigo_fuente: str) -> dict:
    """
    Escanea el código fuente de N-Lang reformulado (con CLASS, VAR, CTRL),
    identifica Clases y sus Subvariables, y asigna el ID de Codificación 
    de Posición Concatenada (CPC).

    Retorna un diccionario mapeando 'Clase' -> [Subvariables y sus IDs].
    """
    
    # --- 1. Expresiones Regulares para la Segmentación ---
    
    # Patrón para la Clase Principal: Aísla la declaración completa de la clase.
    # r'CLASS\s+(\w+)\s*=\s*(.*?);'
    # Grupo 1: Nombre de la Clase (e.g., Inventario)
    # Grupo 2: Contenido del Bloque (e.g., VAR espacio(100), CTRL otra_variable{...})
    patron_clase_principal = re.compile(
        r'CLASS\s+(\w+)\s*=\s*(.*?);', 
        re.DOTALL | re.MULTILINE
    )
    
    # Patrón para CUALQUIER Subvariable dentro del cuerpo de la clase (Grupo 2).
    #
    # Grupo 1: Keyword (VAR o CTRL)
    # Grupo 2: Nombre de la Subvariable
    # Grupo 3: Contenido del Bloque (ej: (100) o {0, total += 1...})
    patron_subvariable = re.compile(
        r'(VAR|CTRL)\s+(\w+)\s*(\(.*?\)|{.*?})', 
        re.DOTALL
    )
    
    tabla_simbolos = {}
    id_clase_contador = 1  # Inicia en 1
    
    # 2. ITERACIÓN PRINCIPAL: CLASES
    for match_clase in patron_clase_principal.finditer(codigo_fuente):
        nombre_clase = match_clase.group(1).strip()
        contenido_bloque = match_clase.group(2).strip() # Contiene las declaraciones internas
        
        # Almacenar la nueva clase en la tabla de símbolos
        tabla_simbolos[nombre_clase] = {
            "id_clase": id_clase_contador,
            "subvariables": []
        }
        
        # El ID local 1 se reserva para la Clase misma.
        id_local_contador = 2 
        
        # 3. PROCESAMIENTO SECUNDARIO: SUBVARIABLES (VAR y CTRL)
        for sub_match in patron_subvariable.finditer(contenido_bloque):
            
            tipo_keyword = sub_match.group(1).strip() # VAR o CTRL
            nombre_sub = sub_match.group(2).strip()
            bloque_sub = sub_match.group(3).strip() # Contiene (valor) o {logica}
            
            # Extraer el contenido interno (sin los delimitadores externos)
            umbral_parametros = bloque_sub[1:-1].strip()
            
            # 4. ASIGNACIÓN DEL ID CPC (Concatenación)
            # Ejemplo: Clase 1 + Local 2 -> ID 12
            id_cpc = int(f"{id_clase_contador}{id_local_contador}")
            
            tabla_simbolos[nombre_clase]["subvariables"].append({
                "nombre": nombre_sub,
                "id_cpc": id_cpc,
                "id_local": id_local_contador,
                "tipo": tipo_keyword, # Almacenamos VAR o CTRL
                "umbral_parametros": umbral_parametros
            })
            
            id_local_contador += 1
            
        id_clase_contador += 1
        
    return tabla_simbolos

def procesar_y_mostrar_simbolos(tabla_simbolos: dict):
    """
    Recorre la tabla de símbolos generada y muestra la información extraída.
    Esto simula el paso de la compilación que utiliza los IDs CPC.
    """
    print("\n" + "="*50)
    print("PROCESAMIENTO DE LA TABLA DE SÍMBOLOS (Fase de Compilación)")
    print("="*50)
    
    for nombre_clase, data_clase in tabla_simbolos.items():
        print(f"\n[CLASE {data_clase['id_clase']}: {nombre_clase}]")
        print("----------------------------------------")
        
        for subvar in data_clase['subvariables']:
            print(f"  > ID CPC: {subvar['id_cpc']}")
            print(f"    Tipo: {subvar['tipo']}")
            print(f"    Nombre: {subvar['nombre']}")
            
            if subvar['tipo'] == 'VAR':
                # Las VARs contienen el valor inicial o el umbral
                print(f"    Umbral/Valor Inicial: {subvar['umbral_parametros']}")
            
            elif subvar['tipo'] == 'CTRL':
                # Las CTRLs contienen la lógica de control y la acción
                print(f"    Lógica de Control: {subvar['umbral_parametros']}")
                
                # Aquí se podría implementar una lógica para separar el umbral (e.g., '1')
                # de la acción (e.g., 'peso_total += "Alerta de peso"')
                partes = [p.strip() for p in subvar['umbral_parametros'].split(',', 1)]
                if len(partes) > 1:
                    print(f"      Umbral Binario: {partes[0]}")
                    print(f"      Acción a Ejecutar: {partes[1]}")
                else:
                    print(f"      Definición Simple: {subvar['umbral_parametros']}")

# Ejemplo de uso con la nueva sintaxis N-Lang:
codigo_ejemplo = """
CLASS Inventario = (
    VAR espacio(100, "el inventario se ha llenado"),
    VAR peso_total(0),
    CTRL control_alerta{1, peso_total += "Alerta de peso"},
    VAR max_peso(500)
);

CLASS Agente = (
    VAR Total(10),
    CTRL control_energia{1, Total += 1, "Se ha acabado la energía"}, 
    VAR bateria(100)
);
"""

print("--- Ejecución del Analizador ---")
simbolos = analizar_codigo_n(codigo_ejemplo)

# Llamada a la nueva función de procesamiento
procesar_y_mostrar_simbolos(simbolos)

