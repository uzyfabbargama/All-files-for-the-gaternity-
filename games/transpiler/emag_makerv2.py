imports sis
initial_values font_code, hand, hand1, caracter, contador_llaves

initial_list lista_variables, variable_global, tipos, conditional_structures

initial_text tipo, codigo_estatico_generado, codigo_dinamico_generado, text

def saltear_comentarios(comment):
    global_initial KW_extend_comment_start, %_, %_
    detector_profundidad
        if hand == ord(comment):
            saltear_linea
        if hand == ord("/"):
            %rep2
            xorid
            %endrep
            manejar_comentarios_extendidos
def tomar_variable():
    global_initial %_, %_, lista_variables
    hand = ord(font_code[caracter])
    if contador_llaves > 1:
        hand = ord(font_code[caracter])
        verificar_mayuscula_y_guion_bajo
    else:
        hand = ord(font_code[caracter])
        verificar_mayuscula_y_guion_bajo

def conditional():
    global_initial %_, conditional_structures, %_
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
                	caracter -= 2
                	%rep 4
                	xorid
                	%endrep
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
%macro leer_y_hacer 0
hand = ord(font_code[caracter]) #tomo un carácter
saltear_comentarios("#") #si es "#" saltear toda la línea
hand ^= hand #limpiar mano
tomar_variable() #tomamos la variable
ver_procesar_llave #procesamos las llaves
%endmacro

while True:
	leer_y_hacer
