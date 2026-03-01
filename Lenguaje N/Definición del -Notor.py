import math
def VAR(NUM, slot, pos, string, inputer): 
    value = (NUM // pos)
    slot = 10 ** (math.log10(value) - 1)
    umbral = slot - ((value // slot) % slot) #para obtener el umbral por si se ha modificado
    value = umbral + slot + inputer #para armar el valor con el input, (con el valor ya modificado)
    CV = (value // slot) % 2 #controlador VAR
    D = 1 - CV #inversor para el detector
    D and print(string) #el corto circuito para aplicar el string
    value += D*slot*pos #reestablecer el controlador (sólo si D es 1) en la posición del número
    return value, slot
def CREATE_VAR(umbral):
    slot = 10 ** (math.log10(umbral) - 1)
    Complemnt = slot - umbral
    value = Complemnt + slot
    return value, slot

def CTRL(NUM, slot, pos, *destinos_y_valores):
    slot = 4
    Value = (NUM // pos) % 4
    Carry = (Value) % 2
    CC = (Value // slot)
    D = 1 - CC
    límite = len(destinos_y_valores)
    destino = 0
    while i < límite:
        destino += destinos_y_valores[i] * destinos_y_valores[i+1] * D
        # comment: el primer valor para el destino, y el segundo para el valor (o viceversa) pero sólo si está el Detector activo
        i += 1
    # end while
    Value = (Carry*2 + D) % 4 #reestablecer el valor)
    return Value, slot, destino
def CREATE_CTRL(Carry):
    Carry %= 2
    Action = 1
    slot = 4
    Value = (Carry*2 + Action)%slot
    return Value, slot

#i = 1
#while i < 6:
    # comment: 
    #print(i)
    #i += 1
# end while

def CLASS(*componentes):
    numeraso_final = 0
    multiplicador_posicion = 1  # Comienza en 1 (la primera variable no se desplaza)
    Pos = []
    # 1. Itera sobre cada componente (VAR o CTRL)
    for valor_componente, tamaño_slot in componentes:

        # 2. Calcula la contribución: Multiplica el valor por su posición actual
        contribucion = valor_componente * multiplicador_posicion
        #Creamos una lista para las posiciones
        Pos.append(multiplicador_posicion) 
        # 3. Acumula la contribución al Numeraso total
        numeraso_final += contribucion
        
        # 4. Actualiza el multiplicador para el siguiente componente
        # El próximo componente debe comenzar en la posición donde termina el actual.
        multiplicador_posicion *= tamaño_slot
        
    # El multiplicador_posicion final es el tamaño total del slot de la clase.
    
    return numeraso_final, multiplicador_posicion, Pos

VAR_espacio_inicial = CREATE_VAR(umbral=100)
Value_CTRL, Slot_CTRL = CREATE_CTRL(Carry=1)
CTRL_para_CLASS = (Value_CTRL, Slot_CTRL) 
VAR_peso_inicial = CREATE_VAR(umbral=10)
Numeraso_Inventario, Slot_Inventario_Total, Pos = CLASS(
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
print("El 'Numeraso_Inventario' contiene ahora todas las variables y controles compilados aritméticamente.")
i = 0
límite = len(Pos)
while i < límite:
    print(f"Posiciones de los elementos = {i}- {Pos[i]}")
    i += 1
#print(límite)

