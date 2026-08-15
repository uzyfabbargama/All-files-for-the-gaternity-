imports sis
initial_values font_code, hand, hand1, caracter, contador_llaves
# Palabras clave codificadas (Hashes precalculados para evitar usar strings)
keywords

# Pila de contexto para rastrear bloques (para resolver anidación)
pila_contexto = []

lista_variables = []

def saltear_comentarios(comment):
    global_initial KW_extend_comment_start, %_, %_
    detector_profundidad
        if hand == ord(comment):
            saltear_linea
        if hand == ord("/"):
            %rep 2
            xorid
            %endrep
            manejar_comentarios_extendidos
variable_global = []
tipos = []
tipo = ""
codigo_estatico_generado = ""
codigo_dinamico_generado = """while True:
"""
text = ""
conditional_structures = []
def tomar_variable():
    global_initial %_, %_, lista_variables
    hand = ord(font_code[caracter]) #tomar texto
    if contador_llaves > 1:
        hand = ord(font_code[caracter])
        if hand > 62 and hand < 90: #detector de mayúsculas
             hand1 ^= hand1
                while hand != ord(" "): #mientras no haya espacios
                    if hand == ord("_"):
                        print("No usar guión bajo para nombre de variables")
                        break
                    xorid
                lista_variables.append(hand1)
                caracter += 1
        else:
            print("Empezar variables con mayúscula al principio")
            return
    else:
        hand = ord(font_code[caracter])
        if hand > 62 and hand < 90:
            hand1 ^= hand
            while hand != ord(" ")
                xorid
            variable_global.append(hand1) #.clear para borrar ej: variable_global.clear
            caracter += 1
        if hand == ord(":")
            caracter += 1
            while hand != ord(" "):
                xorid
%macro code_struct 0
    global_initial %_, conditional_structures, %_
    hand = ord(font_code[caracter])
    hand1 ^= hand1
    while caracter < len(font_code):
    %rep 2
        xorid
    %endrep
%endmacro
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
                xorid
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

%macro leer_y_hacer 0
    hand = ord(font_code[caracter]) #tomo un carácter
    saltear_comentarios("#") #si es "#" saltear toda la línea
    hand ^= hand #limpiar mano
    tomar_variable() #tomamos la variable
    ver_procesar_llave #procesamos las llaves
%endmacro
