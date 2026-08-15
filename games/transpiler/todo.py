
%define i 1
%macro imports 1
import sis
%endmacro

%macro initial_values 5
# El código fuente original en emag-lang
%1 = """#import Keyword

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
%2 = 0      # hand
%3 = 0      # hand 1
%4 = 0      # caracter
%5 = 0      # contador_llaves
%endmacro
%define p 4
%macro initial_list 4
%1 = [] %## lista_variables = []
%2 = [] %## variable_global = []
%3 = [] %## tipos = []
%4 = [] %## conditional_structures = []
endmacro

%define q 4
%macro initial_text 4
%1 = ""
%2 = ""
%3 = ""
%4 = ""
%endmacro

%macro keywords 0
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
%endmacro
%macro detector_profundidad 0
if caracter < len(font_code):
%endmacro
%macro global_initial 3
global caracter, hand, hand1, font_code, %1, KW_extend_comment_end
global hand1, hand, KW_if, font_code, caracter, text, %2, KW_else, KW_for, KW_while
global hand, hand1, caracter, font_code, %3, contador_llaves %## lista_variables
%endmacro
%## uso: global_initial <KW_extend_comment_start> o <conditional_structures>

%macro xorid 0
hand1 ^= hand
hand1 <<= 1
caracter += 1
hand = ord(font_code[caracter])
%endmacro
%macro saltear_linea 0
while hand != 10:
    caracter += 1
    hand = ord(font_code[caracter])
caracter += 1
hand1 ^= hand1
%endmacro

%macro manejar_comentarios_extendidos 0
if hand1 == KW_comment:
    saltear_linea
elif hand1 == KW_extend_comment_start:
    while hand != ord("*"):
        caracter += 1
        hand = ord(font_code[caracter])
    if hand == ord("*"):
        %rep 2
        xorid
        %endrep
        if hand1 == KW_extend_comment_end:
            return
%endmacro

%macro verificar_mayuscula_y_guion_bajo 0
if hand > 62 and hand < 90
	hand1 ^= hand1
	while hand != ord(" "):
		if hand == ord("_")
			print("No usar guión bajo para nombres de variables")
			sys.exit(1)
		xorid
	lista_variables.append(hand1)
	caracter += 1
else:
	print("Empezar variables con mayúscula al principio")
	sys.exit(1)
%endmacro

%macro code_struct 0
    %## global_initial %_, conditional_structures, %_
    hand = ord(font_code[caracter])
    hand1 ^= hand1
    while caracter < len(font_code):
    %rep 2
        xorid
    %endrep
%endmacro
%macro ver_procesar_llave 0
    hand = ord(font_code[caracter])
    if hand == ord("{"):
        contador_llaves += 1
        caracter += 1
    elif hand == ord("}"):
        contador_llaves -= 1
        caracter += 1
%endmacro
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
