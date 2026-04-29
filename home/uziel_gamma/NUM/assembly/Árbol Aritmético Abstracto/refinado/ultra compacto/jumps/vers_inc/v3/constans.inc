;Definir VAR
    %define KW_VAR 0
    %define P_VAR 1
;Definir CTRL
    %define KW_CTRL 1
    %define P_CTRL 2
;Definir CLASS
    %define KW_CLASS 2
    %define P_CLASS 4
;Definir (
    %define KW_PARENTESIS_OPEN 3
    %define P_PARENTESIS_OPEN 8         ;Dejamos 8 bits para contador de profundidad
;Definir ,
    %define KW_COMMA 11
    %define P_COMMA 0X800
;Definir )
    %define KW_PARENTESIS_CLOSE 12
    %define P_PARENTESIS_CLOSE 0X1000   ;Si recibe esto, reduce 1 al contador sólo si hay más que 1
;Definir {
    %define KW_LLAVES_OPEN 13
    %define P_LLAVES_OPEN 0x2000        ;dejamos 8 bits para contador de profundidad
;Definir }
    %define KW_LLAVES_CLOSE 21
    %define P_LLAVES_CLOSE 0x20_0000    ;Si recibe esto, reduce 1 al contador sólo si hay más que 1
;Definir +
    %define KW_ADD 22
    %define P_ADD 0x40_0000
;Definir -
    %define KW_SUB 23
    %define P_SUB 0X80_0000
;Definir *
    %define KW_MUL 24
    %define P_MUL 0x100_0000
;Definir /
    %define KW_DIV 25
    %define P_DIV 0x200_0000
;Definir **
    %define KW_POWER 26
    %define P_POWER 0x400_0000
;Definir ;
    %define KW_SEMICOLON 27
    %define P_SEMICOLON 0x800_0000
;Definir =
    %define KW_EQUAL 28
    %define P_EQUAL 0x1000_0000
;Definir "
    %define KW_COMILLAS 29
    %define P_COMILLAS 0x2000_0000
;Definir [
    %define KW_CORCHETE_OPEN 30
    %define P_CORCHETE_OPEN 0x4000_0000     ;Dejamos 8 bits
;Definir ]
    %define KW_CORCHETE_CLOSE 38
    %define P_CORCHETE_CLOSE 0x20_0000_0000 ;Si recibe esto, reduce 1 al contador sólo si hay más que 1
;Definir .
    %define KW_PUNTO 39
    %define P_PUNTO 0x40_0000_0000
;Definir '
    %define KW_COMILLA 40
    %define P_COMILLA 0x80_0000_0000
;Definir #
    %define KW_COMMENT 41
    %define P_COMMENT 0x100_0000_0000
;Definir :
    %define KW_DIC 42
    %define P_DIC 0x200_0000_0000
;Definir !
    %define KW_NOT 43
    %define P_NOT 0x400_0000_0000
;Definir <
    %define KW_MENOR 44
    %define P_MENOR 0x800_0000_0000
;Definir >
    %define KW_MAYOR 45
    %define P_MAYOR 0x1000_0000_0000
;Definir " "
    %define KW_SPACE 46
    %define P_SPACE 0x2000_0000_0000
;Definir \n (10 EN ASCII)
    %define KW_NEW_LINE 48
    %define P_NEW_LINE 0x8000_0000_0000
;Definir ^
    %define KW_XOR 49
    %define P_XOR 0x1_0000_0000_0000
;Definir &
    %define KW_AND 50
    %define P_AND 0x2_0000_0000_0000
;Definir |
    %define KW_OR 51 
    %define P_OR 0x4_0000_0000_0000
;Definir 0
    %define KW_0 52 
    %define P_0 0x8_0000_0000_0000
;Definir 1
    %define KW_1 53 
    %define P_1 0x10_0000_0000_0000
;Definir 2
    %define KW_2 54 
    %define P_2 0x20_0000_0000_0000
;Definir 3
    %define KW_3 55 
    %define P_3 0x40_0000_0000_0000
;Definir 4
    %define KW_4 56 
    %define P_4 0x80_0000_0000_0000
;Definir 5
    %define KW_5 57 
    %define P_5 0x100_0000_0000_0000
;Definir 6
    %define KW_6 58 
    %define P_6 0x200_0000_0000_0000
;Definir 7
    %define KW_7 59 
    %define P_7 0x400_0000_0000_0000
;Definir 8
    %define KW_8 60 
    %define P_8 0x800_0000_0000_0000
;Definir 9
    %define KW_9 61 
    %define P_9 0x1000_0000_0000_0000
