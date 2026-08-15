import sys

# El código fuente original en emag-lang
font_code = """#import Keyword

Mapa {
	Object : list {
		X : int _
		Y : int _
		Z : int _
		BlockArea : int _
		BlockResistance : int -
		BlockElectronAffinity : int _
		BlockEnergy : int _
	}
}

Personaje {
	Vida : int 20
	Nombre : str _"
	Item : int _
	MoveX : int 0
	MoveY : int 0
	MoveZ : int 0
	X : int 0+MoveX
	Y : int 0+MoveZ
	Z : int 0+MoveY
	SeeX : int X+1
	SeeY : int Y+1
	SeeZ : int Z+1
	SeeMX : int X-1
	SeeMY : int Y-1
	SeeMZ : int Z-1
	reglas : code { // se ejecuta en bucle
		include "movement.emalang"
	}
}
"""

# Variables de estado que actúan como registros físicos
hand = 0        # Registro de lectura actual (Mano 1)
hand1 = 0       # Registro para almacenar el Hash XOR acumulado (Mano 2)
caracter = 0    # Puntero de programa (PC / Program Counter)
contador_llaves = 0

# Tablas de símbolos planos (XOR_ID -> Valor)
variables_estaticas = {}
variables_reactivas = {}

# Palabras clave codificadas (Hashes precalculados para evitar usar strings)
KW_int = 536
KW_list = 1196
KW_str = 684
KW_code = 1842

# Pila de contexto para rastrear bloques (para resolver anidación)
pila_contexto = []

# --- SIMULACIÓN DE MACROS (Funciones en línea de un solo uso para código plano) ---

def MACRO_saltear_comentarios_y_lineas():
    """Equivale a %macro saltear_comentarios. Saltea comentarios de línea '#' o '//'"""
    global caracter, hand
    if caracter < len(font_code):
        hand = ord(font_code[caracter])
        # Saltea '#' o '//'
        if hand == ord("#") or (hand == ord("/") and caracter + 1 < len(font_code) and font_code[caracter+1] == "/"):
            while caracter < len(font_code) and ord(font_code[caracter]) != 10:  # 10 es LF (salto de línea)
                caracter += 1
            if caracter < len(font_code):
                caracter += 1  # Pasar el salto de línea

def MACRO_ver_procesar_llave():
    """Equivale a %macro ver_procesar_llave. Controla el nivel de anidación estática."""
    global caracter, hand, contador_llaves
    if caracter < len(font_code):
        hand = ord(font_code[caracter])
        if hand == ord("{"):
            contador_llaves += 1
            caracter += 1
        elif hand == ord("}"):
            contador_llaves -= 1
            caracter += 1
            if pila_contexto:
                pila_contexto.pop()

# --- FUNCIONES PURAS PARA LA ANIDACIÓN RECURSIVA (SOS) ---

def tomar_variable():
    """
    Toma un nombre de variable, calcula su Hash XOR en hand1 y procesa
    si es una definición global o interna basándose en el nivel de llaves.
    """
    global caracter, hand, hand1, contador_llaves
    
    if caracter >= len(font_code):
        return False

    hand = ord(font_code[caracter])
    
    # Ignorar espacios en blanco iniciales antes de leer la variable
    while caracter < len(font_code) and chr(hand) in " \t\n\r":
        caracter += 1
        if caracter < len(font_code):
            hand = ord(font_code[caracter])
            
    if caracter >= len(font_code):
        return False

    # Detector de Mayúsculas estricto (A-Z es entre 65 y 90)
    if 65 <= hand <= 90:
        hand1 = 0  # Inicializar registro de Hash XOR
        
        while caracter < len(font_code) and hand != ord(" ") and hand != ord(":") and hand != ord("{") and hand != ord("\n") and hand != ord("\t"):
            if hand == ord("_"):
                print("[ERROR] No usar guion bajo para el nombre de las variables.")
                sys.exit(1)
            
            # Tu algoritmo de Hash XOR-shifting
            hand1 ^= hand
            hand1 = (hand1 << 1) & 0xFFFFFFFF  # Mantener dentro de 32 bits para simular registro físico
            
            caracter += 1
            if caracter < len(font_code):
                hand = ord(font_code[caracter])
                
        # Guardar en la pila de contexto de nombres si estamos abriendo un bloque global
        if contador_llaves == 0:
            pila_contexto.clear()
            pila_contexto.append(hand1)
        else:
            # Si es una variable interna, se añade temporalmente para construir el path XOR plano
            if len(pila_contexto) >= contador_llaves:
                pila_contexto[contador_llaves - 1] = hand1
            else:
                pila_contexto.append(hand1)
                
        return True
    else:
        # No es una variable válida o es un token estructural
        return False

def tipado():
    """
    Resuelve el tipo de dato y su valor.
    Si encuentra 'list', entra de manera recursiva (SOS) para procesar el sub-bloque.
    """
    global caracter, hand, hand1, contador_llaves
    
    # Buscar los dos puntos ":"
    while caracter < len(font_code) and hand != ord(":"):
        caracter += 1
        if caracter < len(font_code):
            hand = ord(font_code[caracter])
            
    if hand == ord(":"):
        caracter += 1  # Saltar el ":"
        
        # Leer el tipo de dato (ej: int, str, list, code)
        salteo_temporal = 0
        tipo_str = ""
        if caracter < len(font_code):
            hand = ord(font_code[caracter])
            while chr(hand) in " \t":
                caracter += 1
                hand = ord(font_code[caracter])
            
            # Extraer la palabra del tipo
            while caracter < len(font_code) and chr(hand).isalnum():
                tipo_str += chr(hand)
                caracter += 1
                hand = ord(font_code[caracter])
                
        # Evaluar el tipo usando aproximación de hashes simples de las constantes de texto
        if tipo_str == "int":
            procesar_valor("int")
        elif tipo_str == "str":
            procesar_valor("str")
        elif tipo_str == "code":
            procesar_valor("code")
        elif tipo_str == "list":
            # Saltar espacios hasta la llave
            while caracter < len(font_code) and chr(hand) in " \t\n\r":
                caracter += 1
                hand = ord(font_code[caracter])
            if hand == ord("{"):
                contador_llaves += 1
                caracter += 1
                # SOS: LLAMADA RECURSIVA FRACTAL
                # Procesamos el sub-bloque de la lista de forma recursiva
                ejecutar_analisis_recursivo()

def procesar_valor(tipo):
    """Extrae el valor asignado a la variable y lo clasifica."""
    global caracter, hand
    
    # Saltar espacios
    while caracter < len(font_code) and chr(hand) in " \t":
        caracter += 1
        hand = ord(font_code[caracter])
        
    valor_acumulado = ""
    while caracter < len(font_code) and hand != 10 and hand != 13: # Hasta fin de línea
        # Ignorar comentarios en línea de tipo '//'
        if hand == ord("/") and caracter + 1 < len(font_code) and font_code[caracter+1] == "/":
            break
        valor_acumulado += chr(hand)
        caracter += 1
        hand = ord(font_code[caracter])
        
    valor_acumulado = valor_acumulado.strip()
    
    # Crear el ID de variable plano basado en la pila de XOR-hashes actual
    id_variable_plano = "_" + "_".join([str(x) for x in pila_contexto[:contador_llaves + 1]])
    
    # Clasificar en reactivo o estático
    # Es reactivo si contiene caracteres alfabéticos de operaciones (como "+", "-", etc.) sin comillas
    es_reactivo = False
    if tipo == "int" and valor_acumulado != "_" and valor_acumulado != "-":
        for char in valor_acumulado:
            if char.isalpha():
                es_reactivo = True
                break
                
    if es_reactivo:
        variables_reactivas[id_variable_plano] = valor_acumulado
    else:
        # Normalizar placeholders de input
        if valor_acumulado in ["_", '_"', '-"']:
            valor_acumulado = "None  # Input requerido"
        elif valor_acumulado == "-":
            valor_acumulado = "0"
        variables_estaticas[id_variable_plano] = valor_acumulado

def ejecutar_analisis_recursivo():
    """El motor de análisis sintáctico que coordina las macros y la recursión."""
    global caracter, hand, contador_llaves
    
    while caracter < len(font_code):
        MACRO_saltear_comentarios_y_lineas()
        
        # Guardar posición actual antes de intentar leer variable
        pos_previa = caracter
        
        if tomar_variable():
            tipado()
        else:
            # Si no es variable, ver si es un cierre de llave
            caracter = pos_previa
            MACRO_ver_procesar_llave()
            
        # Si volvimos al nivel cero de llaves tras procesar un bloque recursivo, salimos
        if contador_llaves < len(pila_contexto) and contador_llaves > 0:
            return

# --- INVOCAR EL PROCESO ---
if __name__ == "__main__":
    print("[INFO] Ejecutando el compilador emag-lang (Sin import re)...")
    ejecutar_analisis_recursivo()
    
    # --- GENERAR CÓDIGO PYTHON PLANO DE SALIDA ---
    print("\n# " + "="*45)
    print("# CÓDIGO GENERADO DE EMAG-LANG")
    print("# " + "="*45)
    
    print("\n# Variables de Estado Estáticas (XOR-IDs)")
    for var, val in variables_estaticas.items():
        print(f"{var} = {val}")
        
    print("\n# Variables Reactivas Inicializadas")
    for var in variables_reactivas.keys():
        print(f"{var} = 0")
        
    print("\nwhile True:")
    print("    # Actualizaciones Reactivas de un solo paso")
    for var, formula in variables_reactivas.items():
        # Aquí en la vida real, reemplazamos los nombres cortos por los XOR_IDs del contexto
        # Pero como no usamos 'import re', se haría con tu buscador de sub-strings manual
        print(f"    {var} = {formula}  # Cálculo reactivo")
        
    print("    break  # Un solo tick de simulación")
