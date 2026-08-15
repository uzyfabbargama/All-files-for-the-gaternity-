r0 = 0 # flag condicional
r1 = 0 # valor temporal
r2 = 0 # valor temporal 2
r3 = 0 # puntero en código fuente
r4 = 0 # estructura de data
r5 = 0 # estructura de token if/else/for/while/import/Keyword/Key
r6 = 0 # estructura de tokens 2
r7 = 0 # estructura de llaves
r8 = 0 # xorid_variable
r9 = 0 # valos numérico
r10 = 0
r11 = 0
r12 = 0
r13 = 0
r14 = 0
r15 = 0
r16 = 0
r17 = 0
r18 = 0
r19 = 0
r20 = 0
r21 = 0
r22 = 0
r23 = 0
r24 = 0
r25 = 0
r26 = 0
r27 = 0
r28 = 0
r29 = 0
r30 = 0
r31 = 0

# data
font_code = """import Keyword

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
#constans
KW_if = 1
if_xorword = 360
KW_else = 2
else_xorword = 1078
KW_while = 3
while_xorword = 2642
KW_for = 4
for_xorword = 616
KW_int = 5
int_xorword = 536
KW_list = 6
list_xorword = 1196
KW_str = 7
str_xorword = 684
KW_code = 8
code_xorword = 1842
KW_comment = 9
comment_xorword = 226  #//
KW_extend_comment_start = 10
extend_comment_start_xorword = 232 #/*
KW_extend_comment_end = 11
extend_comment_end_xorword = 246 #*/
KW_print = 12
print_xorword = 2872
KW_import = 13
import_xorword = 4792
KW_Keyword = 14
Keyword_xorword = 14056
KW_Key = 15
Key_xorword = 830
Broad_bit_KW = 4 #0b1111 (4 bits)
%macro leer 1
r1 = ord(%1)
%endmacro
%macro xorid 2
%1 ^= %1
%rep %2
%1 ^= r1
%1 <<= 1
r3 += 1
%endrep
%endmacro
%macro verif 2
%1 ^= %2
r0 = 0x7FFFFFFFFFFFFFFF
r0 += %1 # si es 0, r0 = self, si es >0, r0 = 0x8000000000000000
r0 >>= 63 # si es 0, r0 = 0, si es >0, r0 = 1
r0 &= 1
#r0 ^= 1 # si es 0, r0 = 1, si es >0, r0 = 0
#correct = 0, error = 1
%endmacro
%macro nomatch 3
%1 ^= 1
%1 -= 1 #r0 = 1 = -1 | 0 = 0
%1 &= %2 #pointer font_code
%3 += %1
%1 >> 63 #r0 = -1 = 1 | 0 = 0
%endmacro
%macro adshif 4
%1 -= 1 # si verif correct r0 = 0, entonces r0 = -1, si verif incorrecto, r0 = 1, entonces r0 = 0
%1 &= %2
%3 |= %1 << %4
%endmacro
%macro habilitar_recursión 1
ret = 0
while ret != 1:
%endmacro
%macro fin_recursión 0
r0 += 0x7FFFFFFFFFFFFFFF #verifica zero flag
r0 >>= 63
r0 &= 1
r0 ^= 1
ret = r0
%endmacro

%macro comparator 2
r1 = ord(font_code[r3])
r2 = ord(%1)
r1 ^= r2
r0 = 0x7FFFFFFFFFFFFFFF
r0 += r1
r0 >>= 63
r0 &= 1
r0 ^= %2
%endmacro
%macro ver_paréntesis 0
comparator "(", %_ #negador de condición
while !r0:
	comparator ")", 1 #finaliza cuando hay un ")"
	
%endmacro
while r3 > len(font_code):
	#if
	habilitar_recursión
		leer font_code[r3]
		xorid r2, 2
		verif r2, if_xorword
		no_match r0, 2, r3
		adshif r0, KW_if, r4, Broad_bit_KW
		fin_recursión
	#else
	habilitar_recursión
	leer font_code[r3]
	xorid r2, 4
	verif r2, else_xorword
	no_match r0, 4, r3
	adshif r0, KW_else, r4, Broad_bit_KW
	#for
	habilitar_recursión
		leer font_code[r3]
		xorid r2, 3
		verif r2, for_xorword
		no_match r0, 3, r3
		adshif r0, KW_for, r4, Broad_bit_KW
		fin_recursión
	#while
	habilitar_recursión
		leer font_code[r3]
		xorid r2, 5
		verif r2, while_xorword
		no_match r0, 5, r3
		adshif r0, KW_while, r4, Broad_bit_KW
		fin_recursión
	#import
	leer font_code[r3]
	xorid r2, 5
	verif r2, import_xorword
	no_match r0, 5, r3
	adshif r0, KW_import, r4, Broad_bit_KW
	#Keyword
	leer font_code[r3]
	xorid r2, 6
	verif r2, Keyword_xorword
	no_match r0, 6, r3
	adshif r0, KW_Keyword, r4, Broad_bit_KW
	#Key
	leer font_code[r3]
	xorid r2, 3
	verif r2, Key_xorword
	adshif r0, KW_Key, r4, Broad_bit_KW
