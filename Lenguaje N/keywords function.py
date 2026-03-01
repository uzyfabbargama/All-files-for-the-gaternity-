def CLASS(*componentes):
    """
    Ensambla el Numeraso final de la Clase sumando los componentes (VAR/CTRL).
    
    componentes: Una secuencia de tuplas (Valor, Slot_size) devueltas por VAR() y CTRL().
    """
    
    numeraso_final = 0
    multiplicador_posicion = 1  # Comienza en 1 (la primera variable no se desplaza)
    
    # 1. Itera sobre cada componente (VAR o CTRL)
    for valor_componente, tamaño_slot in componentes:
        
        # 2. Calcula la contribución: Multiplica el valor por su posición actual
        contribucion = valor_componente * multiplicador_posicion
        
        # 3. Acumula la contribución al Numeraso total
        numeraso_final += contribucion
        
        # 4. Actualiza el multiplicador para el siguiente componente
        # El próximo componente debe comenzar en la posición donde termina el actual.
        multiplicador_posicion *= tamaño_slot
        
    # El multiplicador_posicion final es el tamaño total del slot de la clase.
    return numeraso_final, multiplicador_posicion

# --- Ejemplo de Uso (Requiere que VAR y CTRL estén definidos) ---
# Importamos la librería para usar las funciones que has definido
import math

def VAR(umbral, string, input_val):
    slot10 = len(str(umbral))
    Complemnt = 10**slot10 - umbral
    Value = Complemnt + 1*10**slot10
    Value += input_val % 10**slot10 
    
    # Lógica de acarreo (simplificada)
    CV = math.floor(Value / 10**slot10) % 2 
    D = CV - 1 
    Value += D*Complemnt + D*10**slot10 
    D = D and print(string)
    slot_size = 10**slot10 # Tamaño del slot (ej: 1000)
    # print(f"VAR: Value={Value}, Slot={slot_size}")
    return Value, slot_size

def CTRL(Carry, Input, *asignaciones_con_regla):
    # Lógica de slot Invariante (4)
    slot_size = 4
    Value = Carry * 2 + 1  # 1 es el Action bit
    Value += Input % 2
    
    # 1. Calcular la Bandera de Ejecución (Action)
    Action_Flag = (Value % 2) # Simplificamos a un bit
    
    # 2. Calcular la Ejecución Múltiple (Suma Ponderada)
    # Inicialmente, el ejecutable es cero
    ejecutar_formula = 0
    
    # Iterar sobre las asignaciones variables (regla, destino)
    for regla, destino in asignaciones_con_regla:
        # Se asume que destino es la posición (Pos) y regla es el valor a sumar (VAR)
        ejecutar_formula += (regla * destino) 
        
    # El valor final de la acción es la fórmula completa
    # multiplicada por el Action_Flag (0 o 1) para anularla si es necesario.
    ejecutar = Action_Flag * ejecutar_formula
    
    # IMPORTANTE: CTRL solo devuelve su valor y el slot_size fijo a CLASS.
    # El valor 'ejecutar' se usa en el runtime del Numeraso.
    return Value, slot_size, ejecutar

# --- Implementación de la Clase Inventario (Ejemplo de N-Lang) ---
# CLASS Inventario = (VAR espacio(100,"el inventario se ha llenado"));

# Definir los componentes llamando a VAR y CTRL con valores de prueba
# 1. VAR_espacio_inicial devuelve 2 valores (OK para CLASS)
VAR_espacio_inicial = VAR(umbral=100, string="el inventario se ha llenado", input_val=50)

# 2. CTRL_stock_inicial devuelve 3 valores (Value, slot_size, ejecutar)
# Usamos una sintaxis de desempaquetado con el guion bajo (_) para IGNORAR el valor extra 'ejecutar'.
Value_CTRL, Slot_CTRL, _ = CTRL(Carry=1, Input=0)

# Creamos la tupla de 2 elementos que CLASS espera.
CTRL_para_CLASS = (Value_CTRL, Slot_CTRL) 

# 3. VAR_peso_inicial devuelve 2 valores (OK para CLASS)
VAR_peso_inicial = VAR(umbral=10, string="peso_maximo", input_val=3)

# 1. Armar la clase llamando a CLASS con los resultados
# Pasamos la nueva tupla CTRL_para_CLASS de 2 elementos
Numeraso_Inventario, Slot_Inventario_Total = CLASS(
    VAR_espacio_inicial, 
    CTRL_para_CLASS,  # <--- ¡CORREGIDO!
    VAR_peso_inicial
)

# 2. Imprimir el resultado
print("\n" + "="*40)
print("  CONSTRUCCIÓN DEL NUMERASO ARITMÉTICO")
print("="*40)
print(f"VALOR DEL NUMERASO COMPLETO (LA CLASE): {Numeraso_Inventario}")
print(f"TAMAÑO TOTAL DEL SLOT DE LA CLASE: {Slot_Inventario_Total}")
print("El 'Numeraso_Inventario' contiene ahora todas las variables y controles cifrados.")
