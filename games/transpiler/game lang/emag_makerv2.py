imports sis

initial_values font_code, hand, hand1, caracter, contador_llaves
initial_list lista_variables, variable_global, tipos, conditional_structures
initial_text tipo, codigo_estatico_generado, codigo_dinamico_generado, text
keywords

function_saltar_comentario comment
function_tomar_variable
function_tomar_variable
function_tipado

%macro leer_y_hacer 0
hand = ord(font_code[caracter]) #tomo un carácter
saltear_comentarios("#") #si es "#" saltear toda la línea
hand ^= hand #limpiar mano
tomar_variable() #tomamos la variable
ver_procesar_llave #procesamos las llaves
%endmacro

while True:
	leer_y_hacer
