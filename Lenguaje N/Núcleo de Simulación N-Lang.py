import re
import math
import copy

# --- 0. CONSTANTES GLOBALES Y ESTRUCTURA ARITMÉTICA ---
# Utilizamos una base grande para asegurar que los slots no se solapen.
# En una implementación real, esto sería un BigInt.
BASE = 10000 
SLOT_VAR_BASE = BASE # Slot base para las VARs (ej: Umbral maximo 9999)
SLOT_CTRL_SIZE = 4   # Slot fijo de 4 para la bandera binaria del CTRL

# Estructura de Mapeo Global para la simulación
# { 'Inventario.peso_total': {'pos': 1000000, 'slot': 10000, 'tipo': 'VAR', 'accion': None, 'reset': 990} }
POSICION_MAP = {}
ULTIMA_POSICION = 1
NUMERASO_INICIAL = 0

# --- 1. LECTOR / LEXER (Basado en tu codigo 'lexer_NLang.py') ---

def analizar_codigo_n(codigo_fuente: str) -> dict:
    """Escanea el código fuente de N-Lang y retorna la estructura anidada."""
    
    patron_clase_principal = re.compile(
        r'CLASS\s+(\w+)\s*=\s*\((.*?)\);', 
        re.DOTALL | re.MULTILINE
    )
    patron_subvariable = re.compile(
        r'(VAR|CTRL)\s+(\w+)\s*(\\(.*?\\)|{.*?})', 
        re.DOTALL | re.MULTILINE
    )
    
    estructura_n = {}
    
    for match_clase in patron_clase_principal.finditer(codigo_fuente):
        clase_nombre = match_clase.group(1)
        clase_cuerpo = match_clase.group(2)
        
        variables_y_controles = []
        for match_subvar in patron_subvariable.finditer(clase_cuerpo):
            tipo = match_subvar.group(1)
            nombre = match_subvar.group(2)
            # Limpia los paréntesis/llaves y espacios
            parametros_crudos = match_subvar.group(3).strip('(){} \n')
            
            # Divide los parametros (Umbral/Bandera, Accion/Mensaje)
            # Usamos split(',', 1) para capturar toda la acción/mensaje como una sola cadena
            partes = [p.strip() for p in parametros_crudos.split(',', 1)]
            
            subvar_data = {
                'tipo': tipo,
                'nombre': nombre,
                'clase': clase_nombre,
                'parametros_crudos': parametros_crudos,
                'valor_inicial_o_bandera': partes[0],
                'accion_o_mensaje': partes[1] if len(partes) > 1 else None
            }
            variables_y_controles.append(subvar_data)
        
        estructura_n[clase_nombre] = variables_y_controles
        
    return estructura_n

# --- 2. ENSAMBLADOR ARITMÉTICO (VAR, CTRL, CLASS) ---

def VAR_BUILDER(valor_inicial_str, mensaje_alerta=None) -> tuple[int, int, str, int]:
    """
    Construye el mini-Numeraso para un VAR.
    Devuelve: (Value, Slot_Size, Mensaje, Valor_Reset)
    """
    try:
        valor_inicial = int(valor_inicial_str)
    except ValueError:
        # Si el valor inicial no es un número, usamos 0 por defecto.
        valor_inicial = 0

    umbral = SLOT_VAR_BASE - 1 # Asumimos que el umbral máximo es BASE - 1 (9999)
    # Lógica de Umbral: Determinamos el Umbral (la cantidad de "espacio" disponible)
    # Si el valor inicial es mayor que el umbral maximo, tomamos el umbral
    umbral_final = min(umbral, valor_inicial)

    # 1. El Complemento (lo que falta para BASE)
    Complemnt = BASE - umbral_final 
    
    # 2. El Valor Base: Complemento + (1 * BASE)
    # (El 1*BASE asegura que el CV inicial sea 1 si el valor es 0)
    Value = Complemnt + 1 * BASE
    
    # 3. Añadir el valor inicial real (simulando que se ha escrito)
    # En este POC, asumimos que el valor_inicial es el valor actual.
    Value += valor_inicial
    
    slot_size = BASE
    
    # El valor de corrección (lo que se resta al dispararse el CV)
    valor_reset = Complemnt + BASE 
    
    # El CV (Control Value) es el bit en la posición BASE.
    # CV = math.floor(Value / BASE) % 2
    
    return Value, slot_size, mensaje_alerta, valor_reset

def CTRL_BUILDER(bandera_str, accion_str) -> tuple[int, int, str]:
    """
    Construye el mini-Numeraso para un CTRL (solo el binario de control).
    Devuelve: (Value, Slot_Size, Accion_String)
    """
    # La lógica de CTRL es simple: codifica la bandera de control (0 o 1)
    try:
        bandera = int(bandera_str)
    except ValueError:
        bandera = 0
        
    # El valor de CTRL solo codifica la bandera de acción.
    # Usamos 1 bit para la bandera de acción (0 o 1).
    # Usamos 1 bit para el carry (si fuera necesario), pero lo simplificamos a 4 para el slot
    Value = bandera % 2 
    
    slot_size = SLOT_CTRL_SIZE
    
    # La acción se almacena como una cadena de texto para ser procesada en el runtime
    return Value, slot_size, accion_str

def CLASS(*componentes) -> tuple[int, dict]:
    """
    Ensambla el Numeraso final y el Mapa de Posiciones Globales.
    
    componentes: Una secuencia de tuplas (tipo_componente, datos_brutos, valor_construido, slot_size, reset_value)
    """
    global POSICION_MAP, ULTIMA_POSICION, NUMERASO_INICIAL
    
    numeraso_final = 0
    multiplicador_posicion = 1  # Comienza en 1
    
    mapa_actualizado = {}
    
    # 1. Itera sobre cada componente (VAR o CTRL)
    for tipo, datos_brutos, valor_componente, tamaño_slot, valor_reset in componentes:
        
        nombre_completo = f"{datos_brutos['clase']}.{datos_brutos['nombre']}"
        
        # 2. Registra la posición en el mapa global
        mapa_actualizado[nombre_completo] = {
            'tipo': tipo,
            'pos': multiplicador_posicion,
            'slot': tamaño_slot,
            'accion': datos_brutos['accion_o_mensaje'], # La accion/mensaje a ejecutar
            'reset_value': valor_reset,               # El valor de autocorreccion (solo para VAR)
            'valor_inicial': valor_componente % tamaño_slot # Valor actual
        }

        # 3. Calcula la contribución: Multiplica el valor por su posición
        contribucion = valor_componente * multiplicador_posicion
        
        # 4. Acumula la contribución al Numeraso total
        numeraso_final += contribucion
        
        # 5. Actualiza el multiplicador para el siguiente slot
        multiplicador_posicion *= tamaño_slot
        
    POSICION_MAP = mapa_actualizado
    NUMERASO_INICIAL = numeraso_final
    ULTIMA_POSICION = multiplicador_posicion
    
    # El Numeraso final y el mapa de posiciones (el disassembler)
    return numeraso_final, POSICION_MAP

# --- 3. LECTOR ARITMÉTICO (Disassembler) ---

def READ_SLOT(numeraso: int, nombre_var: str) -> int:
    """Extrae el valor actual de un slot específico del Numeraso."""
    if nombre_var not in POSICION_MAP:
        # Simula un error de puntero nulo o slot no encontrado
        # En N-Lang real, esto simplemente devolvería 0 o causaría un carry.
        return 0

    data = POSICION_MAP[nombre_var]
    pos_inicial = data['pos']
    slot_size = data['slot']
    
    # Formula de Desensamblaje: (Numeraso // Posicion_Inicial) % Slot_Size
    # floor division (//) y modulo (%)
    valor_crudo_slot = (numeraso // pos_inicial) % slot_size
    
    # Para VARs, el valor real es el valor_crudo_slot menos el Complemento (BASE)
    if data['tipo'] == 'VAR':
        # Valor real = Valor crudo - (BASE - Umbral) - 1*BASE
        # Como usamos BASE*1 para asegurar el carry, lo restamos para obtener el valor puro.
        valor_real = valor_crudo_slot - data['reset_value'] # El valor de reset ya incluye el 1*BASE
        
        # Aseguramos que el valor no sea negativo debido a la resta.
        return max(0, valor_real)
        
    # Para CTRLs, el valor es simplemente el binario
    return valor_crudo_slot

# --- 4. TRADUCTOR DE ACCIONES (El Compilador de Reglas de CTRL) ---

def traducir_accion_a_formula(accion_str: str, mapa: dict) -> tuple[str, int]:
    """
    Traduce una acción de CTRL (ej. 'peso_total += 10') a la fórmula aritmética:
    (Valor_a_sumar * Posicion_Final)
    
    Retorna: (Nombre_Variable_Destino, Multiplicador_Numeraso)
    """
    if '+= ' not in accion_str:
        return None, 0 # No es una asignación aritmética

    # Ejemplo: 'peso_total += 10'
    destino_nombre, valor_o_funcion_str = accion_str.split('+=')
    destino_nombre = destino_nombre.strip()
    valor_o_funcion_str = valor_o_funcion_str.strip()

    if destino_nombre not in mapa:
        print(f"ERROR: Variable de destino '{destino_nombre}' no encontrada en el mapa.")
        return None, 0

    datos_destino = mapa[destino_nombre]
    posicion_destino = datos_destino['pos']
    
    # Simulación de lectura de valor
    # Por simplicidad, asumimos que solo se suma una constante (ej: 10)
    try:
        valor_a_sumar = int(valor_o_funcion_str)
    except ValueError:
        # Aquí iría la lógica compleja de N-Lang: Ej: si es 'peso()', leer el slot de 'peso'
        print(f"ADVERTENCIA: Acción '{valor_o_funcion_str}' no es constante. Usando valor 1.")
        valor_a_sumar = 1 

    # La Contribución de la Suma Ponderada: Valor * Posición
    multiplicador_numeraso = valor_a_sumar * posicion_destino
    
    return destino_nombre, multiplicador_numeraso

# --- 5. MOTOR DE EJECUCIÓN (El Tick Branchless) ---

def RUN_N_LANG_TICK(numeraso_actual: int, mapa_posiciones: dict) -> tuple[int, list]:
    """
    Simula un ÚNICO TICK de ejecución del N-OS, aplicando VAR y CTRL sin 'if'.
    
    Retorna el Numeraso_Nuevo y la lista de mensajes de alerta.
    """
    
    correccion_total_var = 0  # La suma de las auto-correcciones de los VARs
    accion_total_ctrl = 0     # La suma de las acciones de los CTRLs activos
    mensajes_alerta = []
    
    # ITERACIÓN 1: CÁLCULO DE CORRECCIONES (VARs Auto-Reguladas)
    for nombre, data in mapa_posiciones.items():
        if data['tipo'] == 'VAR':
            
            # 1. Leer el valor del slot (incluye el carry bit, CV)
            valor_con_cv = (numeraso_actual // data['pos']) % data['slot']
            
            # 2. Calcular el CV (Carry Value) y el Detector (D)
            # CV: Es el bit en la posicion BASE. Si el valor supera BASE, CV es 1.
            # En nuestro builder, CV es 1 si el slot no se ha desbordado, 0 si se desbordó.
            # El valor de corrección (data['reset_value']) ya está ajustado para esto.
            
            # Simpleza: Asumimos que si el valor_con_cv es menor que BASE (10000), el CV es 0.
            # El builder asegura que si no hay desbordamiento, el valor_con_cv > BASE.
            # Aquí revertimos el cálculo del D y el CV para hacerlo simple y efectivo.
            
            # Calculamos el Carry Bit (CV) basado en el desbordamiento del slot
            # Si math.floor(Value / BASE) % 2 es 0, significa que se desbordó.
            CV = math.floor(valor_con_cv / BASE) % 2
            
            # Detector (D): D = CV - 1. 
            # Si CV=1 (No desbordado), D=0 (Anula corrección).
            # Si CV=0 (Desbordado), D=-1 (Aplica corrección con resta).
            D = CV - 1 
            
            # 3. Calcular la corrección para este VAR (Multiplicación por D)
            # La corrección es la resta de su valor de reset. Como D es -1, se convierte en resta.
            correccion_slot = D * data['reset_value'] * data['pos']
            
            correccion_total_var += correccion_slot
            
            # 4. Manejo de Mensajes (No-Aritmético, solo para feedback del host)
            # Solo se ejecuta si D es -1 (es decir, CV=0, desbordamiento)
            if D == -1 and data['accion']:
                mensajes_alerta.append(f"ALERTA ARITMÉTICA: {data['accion']}")

    # ITERACIÓN 2: CÁLCULO DE ACCIONES (CTRLs Ponderados)
    for nombre, data in mapa_posiciones.items():
        if data['tipo'] == 'CTRL':
            
            # 1. Leer la bandera de acción del CTRL (Action_Flag)
            action_flag = READ_SLOT(numeraso_actual, nombre) % 2
            
            # 2. Si la bandera está activa (1), parsear la acción.
            if action_flag == 1 and data['accion']:
                
                # Traducir la acción a la fórmula de suma ponderada
                destino, multiplicador = traducir_accion_a_formula(data['accion'], mapa_posiciones)
                
                # Sumar la contribución al total de acciones
                # Como la bandera es 1, la contribución es 1 * multiplicador.
                accion_total_ctrl += multiplicador 
                
                # Manejo de Mensajes (Solo para feedback del host)
                if '\"' in data['accion']:
                    # Si el CTRL tiene un mensaje de texto
                    mensajes_alerta.append(f"CONTROL ACTIVO: {data['accion']}")


    # ÚNICA OPERACIÓN ARITMÉTICA FINAL (El Tick Branchless)
    # Sumamos las correcciones negativas de VARs y las acciones positivas de CTRLs
    numeraso_nuevo = numeraso_actual + correccion_total_var + accion_total_ctrl
    
    return numeraso_nuevo, mensajes_alerta

# --- CÓDIGO DE PRUEBA Y DEMOSTRACIÓN ---

# 1. Código Fuente N-Lang para la simulación
CODIGO_N = """
CLASS Agente = (
    VAR vida(100),
    VAR energia(50),
    CTRL control_correr{1, energia += -5},
    CTRL control_regenerar{0, vida += 2},
    VAR peso_inventario(10) 
);
"""

print("====================================================================")
print("             1. COMPILACIÓN DEL CÓDIGO FUENTE (N-Lang)              ")
print("====================================================================")

# Analizar el código para obtener la estructura
estructura = analizar_codigo_n(CODIGO_N)

# Pre-ensamblar los componentes para la función CLASS
componentes_ensamblaje = []
for clase_nombre, subvariables in estructura.items():
    for subvar in subvariables:
        datos_brutos = subvar
        if subvar['tipo'] == 'VAR':
            # VAR: valor_inicial_str, mensaje_alerta
            value, slot, msg, reset = VAR_BUILDER(subvar['valor_inicial_o_bandera'], subvar['accion_o_mensaje'])
            componentes_ensamblaje.append(('VAR', datos_brutos, value, slot, reset))
        
        elif subvar['tipo'] == 'CTRL':
            # CTRL: bandera_str, accion_str
            value, slot, accion = CTRL_BUILDER(subvar['valor_inicial_o_bandera'], subvar['accion_o_mensaje'])
            componentes_ensamblaje.append(('CTRL', datos_brutos, value, slot, None)) # CTRL no tiene valor de reset

# 2. Ensamblar la Clase Agente
numeraso_actual, mapa_posiciones = CLASS(*componentes_ensamblaje)

print(f"Base Aritmética (BASE): {BASE}")
print(f"NUMERASO INICIAL (BigInt): {numeraso_actual}")
print(f"TAMAÑO TOTAL DEL SLOT: {ULTIMA_POSICION}")
print("-" * 50)
print("TABLA DE POSICIONES (Mapa de Memoria):")
for nombre, data in mapa_posiciones.items():
    valor_actual = READ_SLOT(numeraso_actual, nombre)
    print(f"  {nombre:<20} | Pos: {data['pos']:<10} | Slot: {data['slot']:<6} | VALOR: {valor_actual}")

print("\n====================================================================")
print("             2. EJECUCIÓN DEL N-OS (TICKS SIMULADOS)               ")
print("====================================================================")

# SIMULACIÓN DE TICKS

def simular_tick(tick_num, numeraso):
    """Ejecuta un tick e imprime el estado."""
    print(f"\n--- TICK {tick_num} ---")
    
    # 1. EJECUTAR EL MOTOR BRANCHLESS
    numeraso_nuevo, mensajes = RUN_N_LANG_TICK(numeraso, mapa_posiciones)
    
    # 2. MOSTRAR RESULTADOS
    print(f"Numeraso Antes: {numeraso}")
    print(f"Numeraso Después: {numeraso_nuevo}")
    print(f"Cambio Neto: {numeraso_nuevo - numeraso}")
    
    # Mostrar alertas (solo para feedback, el motor no las necesita)
    if mensajes:
        print("\nAlertas de Control o Umbral:")
        for msg in mensajes:
            print(f"  > {msg}")

    print("\nVALORES DE ESTADO (Leídos por el Host):")
    # Leer y mostrar el nuevo estado
    for nombre in mapa_posiciones.keys():
        nuevo_valor = READ_SLOT(numeraso_nuevo, nombre)
        print(f"  {nombre:<20} | VALOR: {nuevo_valor}")
        
    return numeraso_nuevo

# --- INICIO DE LA SIMULACIÓN ---

# TICK 1: Correr y gastar energía. control_correr está activo (1)
print("\n[EVENTO: Agente inicia el movimiento (control_correr está activo)]")
numeraso_actual = simular_tick(1, numeraso_actual)

# TICK 2: Dejamos el control_correr activo. La energía desciende a 40
print("\n[EVENTO: Se repite el movimiento. La energía desciende.]")
numeraso_actual = simular_tick(2, numeraso_actual)

# TICK 3: Se inyecta una pérdida de energía externa que hace que el slot se desborde
# Modificamos el mapa de posiciones para simular que 'energia' tiene un Umbral bajo (ej: 40)
# (En un sistema real, el Numeraso se modificaría directamente)

# ** Simulación de Umbral Superado (VAR se auto-corrige) **
# Forzamos que la energía se desborde, inyectando un valor negativo grande.
# Esto se simula como un "input externo" en la posición de energía.
# La posición de 'Agente.energia' es 10000. La pérdida es 10000.
# La pérdida de 10000 hace que el valor de 50 (50 + 9950 + 10000 = 20000) se vaya a 10000
# Al ser 10000, floor(10000/10000)%2 = 0 (CV=0). El detector D=-1 se activa.

# Valor a inyectar (simula un golpe que drena toda la energía)
pos_energia = mapa_posiciones['Agente.energia']['pos']
perdida_energia_externa = -1000000 # Un número grande negativo en la posición de energia

numeraso_actual += perdida_energia_externa * pos_energia

print("\n[EVENTO CRÍTICO: La energía cae a 0 o menos. VAR debe autocorregrse.]")
numeraso_actual = simular_tick(3, numeraso_actual)

# TICK 4: El sistema se estabiliza. La energía se reinició y sigue el control_correr
print("\n[EVENTO: El sistema sigue estable. control_correr sigue activo.]")
numeraso_actual = simular_tick(4, numeraso_actual)
