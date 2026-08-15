import sis

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
#variables_estaticas = {}
#variables_reactivas = {}

# Palabras clave codificadas (Hashes precalculados para evitar usar strings)
KW_int = 536
KW_list = 1196
KW_str = 684
KW_code = 1842
KW_if = 360
KW_else = 1078
KW_while = 2642
KW_for = 616
KW_comment = 226  #//
kW_extend_comment_start = 232 #/*
KW_extend_comment_end = 246 #*/

# Pila de contexto para rastrear bloques (para resolver anidación)
pila_contexto = []

lista_variables = []

def saltear_comentarios(comment):
    global caracter, hand, hand1, font_code, KW_extend_comment_start, KW_extend_comment_end
    if caracter < len(font_code):
        if hand == ord(comment):
            while hand != 10:
                caracter += 1
                hand = ord(font_code[caracter])
            caracter += 1
            hand1 ^= hand1
        if hand == ord("/"):
            %rep 2
            hand1 ^= hand # toma "/" | toma * o /
            hand1 <<= 1 # lo desplaza | lo desplaza
            caracter += 1 #aumenta el counter | aumenta el counter
            hand = ord(font_code[caracter]) #toma otro caracter | toma otro caracter
            %endrep
            
            if hand1 == KW_comment:
                while hand != 10:
                    caracter += 1
                    hand = ord(font_code[caracter])
            elif hand1 == KW_extend_comment_start:
                while hand != ord("*"):
                    caracter += 1
                    hand = ord(font_code[caracter])
                if hand == ord("*"):
                    %rep 2
                    hand1 ^= hand # toma "/" | toma * o /
                    hand1 <<= 1 # lo desplaza | lo desplaza
                    caracter += 1 #aumenta el counter | aumenta el counter
                    hand = ord(font_code[caracter]) #toma otro caracter | toma otro caracter
                    %endrep
                    if hand1 == KW_extend_comment_end:
                        return
variable_global = []
tipos = []
tipo = ""
codigo_estatico_generado = ""
codigo_dinamico_generado = """while True:
"""
text = ""
conditional_structures = []
def tomar_variable():
    global hand, hand1, font_code, caracter
    hand = ord(font_code[caracter]) #tomar texto
    if contador_llaves > 1:
        hand = ord(font_code[caracter])
        if hand > 62 and hand < 90: #detector de mayúsculas
             hand1 ^= hand1
                while hand != ord(" "): #mientras no haya espacios
                    if hand == ord("_"):
                        print("No usar guión bajo para nombre de variables")
                        break
                    hand1 ^= hand
                    hand1 <<= 1
                    caracter += 1
                    hand = ord(font_code[caracter])
                lista_variables.append(hand1)
                caracter += 1
        else:
            print("Empezar variables con mayúscula al principio")
            return
    else:
        hand = ord(font_code[caracter])
        if hand > 62 and hand < 90:
            hand1 ^= hand
            while hand != ord(" ");
                hand1 ^= hand
                hand1 <<= 1
                caracter += 1
                hand = ord(font_code[caracter])
            variable_global.append(hand1) #.clear para borrar ej: variable_global.clear
            caracter += 1
        if hand == ord(":")
            caracter += 1
            while hand != ord(" "):
                hand1 ^= hand #xoreramos
                hand1 <<= 1 #desplazamos
                caracter += 1 #avanzamos
                hand = ord(font_code[caracter]) #tomamos el siguiente byte
def code_struct():
    global hand, hand1, caracter, font_code, conditional_structures, text
    hand = ord(font_code[caracter])
    hand1 ^= hand1
    while caracter < len(font_code):
    %rep 2
        hand1 ^= hand #xoreramos
        hand1 <<= 1 #desplazamos
        caracter += 1 #avanzamos
        hand = ord(font_code[caracter]) #tomamos el siguiente byte
    %endrep
def conditional():
    if hand1 == KW_if:
        hand = ord(font_code[caracter])
        if hand == ord("("): #ver paréntesis
            while hand != ord(")"):
                text += font_code[caracter]
                caracter += 1
                hand = ord(font_code[caracter])
            conditional_structures.append(text)
            hand = ord(font_code[caracter])
            if hand == ord("{"): # el cuerpo
                while hand != ord("}"):
                    text += font_code[caracter]
                    caracter += 1
                    hand = ord(font_code[caracter])
                conditional_structures.append(text)
                text = chr(ord(text[0]) & 0) # destructor de texto
                hand1 ^= hand1
                %rep 2
                hand1 ^= hand #xoreramos
                hand1 <<= 1 #desplazamos
                caracter += 1 #avanzamos
                hand = ord(font_code[caracter]) #tomamos el siguiente byte
                %endrep
                if hand1 == KW_if:
                	conditional()
                elif hand1 == KW_else:
                	conditional()
    elif hand1 == KW_while:
        hand = ord(font_code[caracter])
        if hand == ord("("): #ver paréntesis
            while hand != ord(")"):
                text += font_code[caracter]
                caracter += 1
                hand = ord(font_code[caracter])
            conditional_structures.append(text)
            hand = ord(font_code[caracter])
            if hand == ord("{"): # el cuerpo
            while hand != ord("}"):
                text += font_code[caracter]
                caracter += 1
                hand = ord(font_code[caracter])
            conditional_structures.append(text)
            text = chr(ord(text[0]) & 0) # destructor de texto
    elif hand1 == KW_for:
        hand = ord(font_code[caracter])
        if hand == ord("("): #ver paréntesis
            while hand != ord(")"):
                text += font_code[caracter]
                caracter += 1
                hand = ord(font_code[caracter])
            conditional_structures.append(text)
            hand = ord(font_code[caracter])
            if hand == ord("{"): # el cuerpo
            while hand != ord("}"):
                text += font_code[caracter]
                caracter += 1
                hand = ord(font_code[caracter])
            conditional_structures.append(text)
            text = chr(ord(text[0]) & 0) # destructor de texto
def tipado():
        global hand, hand1
        caracter += 1
        if hand == KW_int:
            tipo = "int"
        elif hand == KW_str:
            tipo = "str"
        elif hand == KW_list:
            caracter += 1
            if hand == ord(":")
                #ver llaves
                caracter += 1
                hand = ord(font_code[caracter])
                if hand == ord("{"):
                    contador_llaves += 1
                    caracter += 1
                elif hand == ord("}"):
                    contador_llaves -= 1
                    caracter += 1
                    tomar_variable()
                    tipado()
        elif hand == KW_code:
            code_struct()

contador_llaves = 0
%macro ver_procesar_llave 0
    hand = ord(font_code[caracter])
    if hand == ord("{"):
        contador_llaves += 1
        caracter += 1
    elif hand == ord("}"):
        contador_llaves -= 1
        caracter += 1
%endmacro

%macro generar_fuente_python 1
    
%endmacro
%macro leer_y_hacer 0
    hand = ord(font_code[caracter]) #tomo un carácter
    saltear_comentarios "#" #si es "#" saltear toda la línea
    hand ^= hand #limpiar mano
    tomar_variable() #tomamos la variable
    ver_procesar_llave #procesamos las llaves
%endmacro
