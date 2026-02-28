;SHL 0b10 = 100
;SHR 0b10 = 1
section .data:
    INPUT db "VAR x (50)", 0x0a ;código de entrada
;PE (propósito geneal)
;PE (propósito específico)
;registros temporales
    ;rax PG #comparación
    ;rcx PG #libre
    ;rdx PG #para guardar bytes
    ;rsi PE 
    ;rdi PE 
    ;r8 PG #libre
    ;r9 PG #operador
    ;r10 PG #resultado del super_if
    ;r11 PG #contador cifras
    mov r11, 10000
;registros permanentes
    ;rbx PG #se une a R13, para guardar el umbral y valor de cada variable, (hasta 15 bits (de 0 a 15) por cada variable, para el valor, y un último bit para el umbral) = 4 variables por registro
    ;rsp PE
    ;rbp PE
    ;r12 PG (contador de página para RBX) (se conectará en RAM para guardar hasta 16 páginas (4 × 16 = 64 variables) lo que permite SIMD natural)
    ;r13 PG Contexto nombres (Almacena un total de 64 variables (1 variable por bit))
    ;r14 PG (se usa r14B, para contar las variables usadas) (bueno, se usará)
    ;r15 PG #contexto keywords 1-27

;lista keywords
    ;1     ;"VAR"          ;Keyword: VAR
    ;2     ;"CTRL"         ;Keyword CTRL
    ;3     ;"CLASS"        ;Keyword CLASS
    ;4     ;"("            ;Subkeyword VAR-init
    ;5     ;","            ;Subkeyword VAR-middle (depende de "(" para una extensión o ")" para un fin)
    ;6     ;")"            ;Subkeyword VAR-end
    ;7     ;"{"            ;Subkeyword CTRL-init
    ;8     ;"}"            ;Subkeyword CTRL-end (depende la ",")
    ;9     ;"+"            ;Subkeyword add
    ;10     ;"-"           ;Subkeyword sub
    ;11    ;"*"            ;Subkeyword mul/shl
    ;12    ;"/"            ;Subkeyword div/shr
    ;13    ;"**"           ;Subkeyword power
    ;14    ;";"            ;Subkeyword end-CLASS
    ;15    ;"="            ;Subkeyword equal
    ;16    ;'"'            ;Subkeyword string1
    ;17 "["                 ;keyword load and save (start)
    ;18 "]"                 ;keyword load and save (end)
    ;19 "."                 ;keyword extension save/load
    ;20 "'"                 ;Subkeyword string2
    ;#" no hace falta, ya que la condición: hacer nada y/o ignorar es gratuita
    ;Error, el # no es simplemente "hacer nada" es "ignorar hasta recibir un salto de línea" 
    ;21 "#"                 ;Coemntarios
    ;22 ";"                 ;Otra Subekeyword de asignación y/o división
    ;23 "!"                 ;subkeyword para not
    ;24 "<"                 ;subkeyword para mayor qué
    ;25 ">"                 ;subkeyword para menor qué
    ;26 " "                 ;subkeyword para delimitar variables
    ;27 "e"					;subkeyword para errores
    ;28 "\n"                ;salto de línea
    ;29 "^"                 ;xor
    ;30 "&"                 ;and
    ;31 "|"                 ;or
    ;32 "1"                 ;1
    ;33 "2"                 ;2
    ;34 "3"                 ;3
    ;35 "4"                 ;4
    ;36 "5"                 ;5
    ;37 "6"                 ;6
    ;38 "7"                 ;7
    ;39 "8"                 ;8
    ;40 "9"                 ;9
    ;41 "0"                 ;0
;
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
    %define P_PARENTESIS_OPEN 8
;Definir ,
    %define KW_COMMA 4
    %define P_COMMA 0X10
;Definir )
    %define KW_PARENTESIS_CLOSE 5
    %define P_PARENTESIS_CLOSE 0X20
;Definir {
    %define KW_LLAVES_OPEN 6
    %define P_LLAVES_OPEN 0X40
;Definir }
    %define KW_LLAVES_CLOSE 7
    %define P_LLAVES_CLOSE 0X80
;Definir +
    %define KW_ADD 8
    %define P_ADD 0X100
;Definir -
    %define KW_SUB 9
    %define P_SUB 0X200
;Definir *
    %define KW_MUL 10
    %define P_MUL 0X400
;Definir /
    %define KW_DIV 11
    %define P_DIV 0x800
;Definir **
    %define KW_POWER 12
    %define P_POWER 0x1000
;Definir ;
    %define KW_SEMICOLON 13
    %define P_SEMICOLON 0x2000
;Definir =
    %define KW_EQUAL 14
    %define P_EQUAL 0x4000
;Definir "
    %define KW_COMILLAS 15
    %define P_COMILLAS 0x8000
;Definir [
    %define KW_CORCHETE_OPEN 16
    %define P_CORCHETE_OPEN 0x1_0000
;Definir ]
    %define KW_CORCHETE_CLOSE 17
    %define P_CORCHETE_CLOSE 0x2_0000
;Definir .
    %define KW_PUNTO 18
    %define P_PUNTO 0x4_0000
;Definir '
    %define KW_COMILLA 19
    %define P_COMILLA 0x8_0000
;Definir #
    %define KW_COMMENT 20
    %define P_COMMENT 0x10_0000
;Definir :
    %define KW_DIC 21
    %define P_DIC 0x20_0000
;Definir !
    %define KW_NOT 22
    %define P_NOT 0x40_0000
;Definir <
    %define KW_MENOR 23
    %define P_MENOR 0x80_0000
;Definir >
    %define KW_MAYOR 24
    %define P_MAYOR 0x100_0000
;Definir " "
    %define KW_SPACE 25
    %define P_SPACE 0x200_0000
;Definir e
    %define KW_ERROR 26
    %define P_ERROR 0x400_0000
;Definir \n (10 EN ASCII)
    %define KW_NEW_LINE 27 
    %define P_NEW_LINE 0x800_0000
;Definir ^
    %define KW_XOR 28
    %define P_XOR 0x1000_0000
;Definir &
    %define KW_AND 29
    %define P_AND 0x2000_0000
;Definir |
    %define KW_OR 30 
    %define P_OR 0x4000_0000
;Definir 0
    %define KW_0 31 
    %define P_0 0x8000_0000
;Definir 1
    %define KW_1 32 
    %define P_1 0x1_0000_0000
;Definir 2
    %define KW_2 33 
    %define P_2 0x2_0000_0000
;Definir 3
    %define KW_3 34 
    %define P_3 0x4_0000_0000
;Definir 4
    %define KW_4 35 
    %define P_4 0x8_0000_0000
;Definir 5
    %define KW_5 36 
    %define P_5 0x10_0000_00000
;Definir 6
    %define KW_6 37 
    %define P_6 0x20_0000_0000
;Definir 7
    %define KW_7 38 
    %define P_7 0x40_0000_00000
;Definir 8
    %define KW_8 39 
    %define P_8 0x80_0000_0000
;Definir 9
    %define KW_9 40 
    %define P_9 0x100_0000_0000
;Definir: Lista → nombres: CTRL, VAR, CLASS


_start:
;Parser[0]
    %macro xorid_64 1
    %assign %%hash 0
    %strlen %%largo %1
    %assign %%i 1
    %rep %%largo
        %substr %%char %1 %%i
        %assign %%hash ((%%hash ^ %%char) << 1)
        %assign %%i %%i + 1
    %endrep
    dq %%hash    ; Guardamos el ID final como 64 bits (8 bytes)
%macroend
%assign total_vars 0

%macro DECLARAR_VAR 1
    %assign %%largo 0
    %strlen %%largo %1
    
    ; Calculamos el XORID del nombre (ej: "x")
    %assign %%hash 0
    %assign %%i 1
    %rep %%largo
        %substr %%char %1 %%i
        %assign %%hash ((%%hash ^ %%char) << 1)
        %assign %%i %%i + 1
    %endrep

    ; Guardamos los datos en la sección .data
    section .data
        var_id_%+ total_vars: dq %%hash       ; El ID numérico
        var_bit_%+ total_vars: dq (1 << total_vars) ; Su posición en R13
    
    %assign total_vars total_vars + 1
%macroend

; Uso:
DECLARAR_VAR "x"  ; Asigna Bit 0
DECLARAR_VAR "y"  ; Asigna Bit 1
DECLARAR_VAR "temp" ; Asigna Bit 2
    %macro super_if2(2)   ;**
            mov rax, %2   ;Resultado éxito
            mov r10, 0    ;Resultado fallo
            ; Check *
            mov r9b, INPUT
            shl r9, 8           ;Preparar para "*"
            cmovnz rax, r10
            ; Check *
            mov r9b, INPUT[rsi+1]
            xor r9, %1
            cmovnz rax, r10
    %endmacro
    %macro super_if3 (1)
        mov rax, %2         ;Resultado de Éxito
        mov r10, 0	        ;Registro de Fallo
    ;Check 'V'
        or r9b, INPUT[rsi]	    ;Cargar 'V'
        shl r9, 8           ;Preparar para "A"
    ;Check 'A'
        or r9b, INPUT[rsi+1]   ;Cargar 'A'
        shl r9, 8           ;Preparar para "R"
    ;Check 'R'
        or r9b, INPUT[rsi+2]   ;Cargar 'R'
        xor r9, %1     	;Si coincide, r9 = 0
        cmovnz rax, r10  	; Si falla (r9 != 0), rax = 0.
    %endmacro
    %macro super_if4 (2)
            mov rax, %2          ;Resultado de Éxito
            mov r10, 0	        ;Registro de Fallo
            ;Check 'C'
            mov r9b, INPUT[rsi] 	; Cargar 'C'
            shl r9, 8           ;Preparar para "T"
            ;Check 'T'
            mov r9b, INPUT[rsi+1]	; Cargar 'T'
            shl r9, 8           ;Preparar para "R"
            ; Check 'R'
            mov r9b, INPUT[rsi+2]	; Cargar 'R'
            shl r9, 8           ;Preparar para "L"
            ; Check 'L'
            mov r9b, INPUT[rsi+3]	; Cargar 'L'
            xor r9, %1  		; Detectar byte
            cmovnz rax, r10		; Comparar byte
    %endmacro
    %macro super_if5 (2)
            mov rax, %2         ;Resultado de éxito
            mov r10, 0          ;Registro de Fallo        
            ;Check C
            mov r9b, INPUT[rsi]    ;Cargar "C"
            shl r9, 8           ;Preparar para "L"
            ; Check L 
            mov r9b, INPUT[rs+1]
            shl r9, 8           ;Preparar para "A"
            ; Check A 
            mov r9b, INPUT[rsi+2]
            shl r9, 8           ;Preparar para "S"
            ; Check S 
            mov r9b, INPUT[rsi+3]
            shl r9, 8           ;Preparar para "S"
            ; Check S
            mov r9b, INPUT[rsi+4]
            xor r9, %1
            cmovnz rax, r10
    %endmacro
    %macro super_if6 (2) ;valor, Pos
             mov rax, %2        ;Resultado de éxito
            mov r10, 0          ;Registro de Fallo        
            ;Check 1
            mov r9b, INPUT[rsi]
            shl r9, 8           ;Preparar para "2"
            ; Check 2 
            mov r9b, INPUT[rsi+1]
            shl r9, 8           ;Preparar para "3"
            ; Check 3 
            mov r9b, INPUT[rsi+2]
            shl r9, 8           ;Preparar para "4"
            ; Check 4 
            mov r9b, INPUT[rsi+3]
            shl r9, 8           ;Preparar para "5"
            ; Check 5
            mov r9b, INPUT[rsi+4]
            shl r9, 8           ;Preparar para "6"
            ; Check 6
            mov r9b, INPUT[rsi+5]
            xor r9, %1
            cmovnz rax, r10
    %endmacro
    %macro super_if7 (2)
            mov rax, %2         ;Resultado de éxito
            mov r10, 0          ;Registro de Fallo        
            ;Check 1
            mov r9b, INPUT[rsi]
            shl r9, 8           ;Preparar para "2"
            ; Check 2 
            mov r9b, INPUT[rsi+1]
            shl r9, 8           ;Preparar para "3"
            ; Check 3 
            mov r9b, INPUT[rsi+2]
            shl r9, 8           ;Preparar para "4"
            ; Check 4 
            mov r9b, INPUT[rsi+3]
            shl r9, 8           ;Preparar para "5"
            ; Check 5
            mov r9b, INPUT[rsi+4]
            shl r9, 8           ;Preparar para "6"
            ; Check 6
            mov r9b, INPUT[rsi+5]
            shl r9, 8           ;Preparar para "7"
            ; Check 7
            mov r9b, INPUT[rsi+6]
            xor r9, %1
            cmovnz rax, r10
    %endmacro
    %macro super_if8 (2)
            mov rax, %2         ;Resultado de éxito
            mov r10, 0          ;Registro de Fallo        
            ;Check 1
            mov r9b, INPUT[rsi]
            shl r9, 8           ;Preparar para "2"
            ; Check 2 
            mov r9b, INPUT[rsi+1]
            shl r9, 8           ;Preparar para "3"
            ; Check 3 
            mov r9b, INPUT[rsi+2]
            shl r9, 8           ;Preparar para "4"
            ; Check 4 
            mov r9b, INPUT[i+3]
            shl r9, 8           ;Preparar para "5"
            ; Check 5
            mov r9b, INPUT[i+4]
            shl r9, 8           ;Preparar para "6"
            ; Check 6
            mov r9b, INPUT[i+5]
            shl r9, 8           ;Preparar para "7"
            ; Check 7
            mov r9b, INPUT[i+6]
            shl r9, 8           ;Preparar para "8"
            ; Check 8
            mov r9b, INPUT[i+7]
            xor r9, %1
            cmovnz rax, r10
    %endmacro
    %macro if(2)
        mov rax, 0
        mov r10, %1         ;Para guardar
        mov r9, INPUT       ;Para comparar
        xor r9, %2          ;INPUT vs valor_real
        cmovnz rax, r10     ;
    %endmacro
    %macro do_in 1
    xor %1, rax
    %endmacro
    ;Name List
        ;1
        %define name_1 0
        %define pos_1 0x1
        ;B
        %define name_1 1
        %define pos_1 0x2
        ;C
        %define name_2 2
        %define pos_2 0x4
        ;D
        %define name_3 3
        %define pos_3 0x8
        ;E
        %define name_4 4
        %define pos_4 0x10
        ;F
        %define name_5 5
        %define pos_5 0x20
        ;G
        %define name_6 6
        %define pos_6 0x40
        ;H
        %define name_7 7
        %define pos_7 0x80
        ;I
        %define name_8 8
        %define pos_8 0x100
        ;J
        %define name_9 9
        %define pos_9 0x200
        ;K
        %define name_10 10
        %define pos_10 0x400
        ;L
        %define name_11 11
        %define pos_11 0x800
        ;M
        %define name_12 12
        %define pos_12 0x1000
        ;N
        %define name_13 13
        %define pos_13 0x2000
        ;O
        %define name_14 14
        %define pos_14 0x4000
        ;P
        %define name_15 15
        %define pos_15 0x8000
        ;Q
        %define name_16 16
        %define pos_16 0x1_0000
        ;R
        %define name_17 17
        %define pos_17 0x2_0000
        ;S
        %define name_18 18
        %define pos_18 0x4_0000
        ;T
        %define name_19 19
        %define pos_19 0x8_0000
        ;U
        %define name_20 20
        %define pos_20 0x10_0000
        ;V
        %define name_21 21
        %define pos_21 0x20_0000
        ;W
        %define name_22 22
        %define pos_22 0x40_0000
        ;X
        %define name_23 23
        %define pos_23 0x80_0000
        ;Y
        %define name_24 24
        %define pos_24 0x100_0000
        ;Z
        %define name_25 25
        %define pos_25 0x200_0000
        ;a
        %define name_26 26
        %define pos_26 0x400_0000
        ;b
        %define name_27 27
        %define pos_27 0x800_0000
        ;c
        %define name_28 28
        %define pos_28 0x1000_0000
        ;d
        %define name_29 29
        %define pos_29 0x2000_0000
        ;e
        %define name_30 30
        %define pos_30 0x4000_0000
        ;f
        %define name_31 31
        %define pos_31 0x8000_0000
        ;g
        %define name_32 32
        %define pos_32 0x1_0000_0000
        ;h
        %define name_33 33
        %define pos_33 0x2_0000_0000
        ;i
        %define name_34 34
        %define pos_34 0x4_0000_0000
        ;j
        %define name_35 35
        %define pos_35 0x8_0000_0000
        ;k
        %define name_36 36
        %define pos_36 0x10_0000_0000
        ;l
        %define name_37 37
        %define pos_37 0x20_0000_0000
        ;m
        %define name_38 38
        %define pos_38 0x40_0000_0000
        ;n
        %define name_39 39
        %define pos_39 0x80_0000_0000
        ;o
        %define name_40 40
        %define pos_40 0x100_0000_0000
        ;p
        %define name_41 41
        %define pos_41 0x200_0000_0000
        ;q
        %define name_42 42
        %define pos_42 0x400_0000_0000
        ;r
        %define name_43 43
        %define pos_43 0x800_0000_0000
        ;s
        %define name_44 44
        %define pos_44 0x1000_0000_0000
        ;t
        %define name_45 45
        %define pos_45 0x2000_0000_0000
        ;u
        %define name_46 46
        %define pos_46 0x4000_0000_0000
        ;v
        %define name_47 47
        %define pos_47 0x8000_0000_0000
        ;w
        %define name_48 48
        %define pos_48 0x1_0000_0000_0000
        ;x
        %define name_49 49
        %define pos_49 0x2_0000_0000_0000
        ;y
        %define name_50 50
        %define pos_50 0x4_0000_0000_0000
        ;z
        %define name_51 51
        %define pos_51 0x8_0000_0000_0000
        ;slot52
        %define name_52 52
        %define pos_52 0x10_0000_0000_0000
        ;slot53
        %define name_53 53
        %define pos_53 0x20_0000_0000_0000
        ;slot54
        %define name_54 54
        %define pos_54 0x40_0000_0000_0000
        ;slot 55
        %define name_55 55
        %define pos_55 0x80_0000_0000_0000
        ;slot 56
        %define name_56 56
        %define pos_56 0x100_0000_0000_0000
        ;slot 57
        %define name_57 57
        %define pos_57 0x200_0000_0000_0000
        ;slot 58
        %define name_58 58
        %define pos_58 0x400_0000_0000_0000
        ;slot 59
        %define name_59 59
        %define pos_59 0x800_0000_0000_0000
        ;slot 60
        %define name_60 60
        %define pos_61 0x1000_0000_0000_0000
        ;slot 61
        %define name_61 61
        %define pos_61 0x2000_0000_0000_0000
        ;slot 62
        %define name_62 62
        %define pos_62 0x4000_0000_0000_0000
        ;slot 63
        %define name_63 63
        %define pos_63 0x8000_0000_0000_0000

    %macro detectar (3)
    super_if%1 %2, pos_%3 ;%1 = cantidad de bytes, %2 bytes, %3 valor pos
    do_in r13
    %macro Lista_variables (2) ;2% ubicación, %1 nombre
    if pos_%2, %1
    do_in r13
    %endmacro
    ;nif_checker[0]
        ;if["VAR"]
        super_if3 ("VAR", P_VAR)
            ;do
            do_in r15;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        super_if4 ("CTRL", P_CTRL)
            ;do
            do_in r15;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        super_if5 ("CLASS", P_CLASS)
            ;do
            do_in r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        if P_PARENTESIS_OPEN,"("
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        if P_COMMA, ","
            ;do
            do_in r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        if P_PARENTESIS_CLOSE, ")"
            ;do
            do_in r15;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        if P_LLAVES_OPEN, "{"
            ;do
            do_in r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        if P_LLAVES_CLOSE, "}"
        ;do
            do_in r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        if P_ADD, "+"
        ;do
            do_in r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        if P_SUB, "-"
            ;do
            do_in r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        if P_MUL, "*"
            ;do
            do_in r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        if P_DIV, "/"
            ;do
            do_in r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        super_if2 ("**", P_POWER)
            ;do
            do_in r15;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        if P_SEMICOLON, ";"
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
        ;if("=")
        if P_EQUAL, "="
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        if P_COMILLAS,'"'
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
        ;if("[")
        if P_CORCHETE_OPEN,"["
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
        ;if("]")
        if P_CORCHETE_CLOSE, "]"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
        ;if('.')
        if P_PUNTO, "."
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
        ;if("'")
            if P_COMILLA, "'"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
        ;if("#")
            if P_COMMENT, "#"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
        ;if(':')
            if P_DIC, ":"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
        ;if('!')
            if P_NOT, "!"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
        ;if("<")
            if P_MENOR, "<"
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(">")
            if P_MAYOR, ">"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(" ")
            if P_SPACE, " "
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
		;if("e")
            if P_ERROR, "e"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if("\n" (10))
            if P_NEW_LINE, 10
            ;DO
            do_in r15
        ;if("^")
            if P_XOR, "^"
            ;DO
            do_in r15
        ;if("&" (10))
            if P_AND, "&"
            ;DO
            do_in r15
        ;if("|")
            if P_OR, "|"
            ;DO
            do_in r15
        ;if("1")
            if P_1, "1"
            ;DO
            do_in r15
        ;if("2")
            if P_2, "2"
            ;DO
            do_in r15
        ;if("3")
            if P_3, "3"
            ;DO
            do_in r15
        ;if("4")
            if P_4, "4"
            ;DO
            do_in r15
        ;if("5")
            if P_5, "5"
            ;DO
            do_in r15
        ;if("6")
            if P_6, "6"
            ;DO
            do_in r15
        ;if("7")
            if P_7, "7"
            ;DO
            do_in r15
        ;if("8")
            if P_8, "8"
            ;DO
            do_in r15
        ;if("9")
            if P_9, "9"
            ;DO
            do_in r15
        ;if("0")
            if P_0, "0"
            ;DO
            do_in r15
;);

;Actualizar y comparar, mediante xor zf
    %define verdad 1
    %macro UPDATE_KW 2 
        mov r9, r15      ;obtener el mapa completo
        xor r9, %2        ;Si es 0 no lo destruye, si es 1, si    
        shr r9, %1       ;desplazado r9 para el tipo de keyword
        and r9, 0x1      ;toma un solo bit
        xor r15, r9     ;Reinicia estado de 1 → 0
        ;Si condición: 0 + keyword 1 = keyword 1
        ;Si condición: 1 + keyword 1 = keyword 0
    %endmacro
        ;UPDATE_KW KW_0, condición
        ;Actualiza la keyword 0
        ;UPDATE_KW KW_9, condición
        ;Actualiza la keyword 9
        ;UPDATE_KW KW_8, condición
        ;Actualiza la keyword 8
        ;UPDATE_KW KW_7, condición
        ;Actualiza la keyword 7
        ;UPDATE_KW KW_6, condición
        ;Actualiza la keyword 6
        ;UPDATE_KW KW_5, condición
        ;Actualiza la keyword 5
        ;UPDATE_KW KW_4, condición
        ;Actualiza la keyword 4
        ;UPDATE_KW KW_3, condición
        ;Actualiza la keyword 3
        ;UPDATE_KW KW_2, condición
        ;Actualiza la keyword 2
        ;UPDATE_KW KW_1, condición
        ;Actualiza la keyword 1
        ;UPDATE_KW KW_OR, condición
        ;Actualiza la keyword or
        ;UPDATE_KW KW_AND, condición
        ;Actualiza la keyword and
        ;UPDATE_KW KW_XOR, condición
        ;Actualiza la keyword xor
        ;UPDATE_KW KW_NEW_LINE, condición
        ;Actualiza la keyword nueva_línea
        ;UPDATE_KW KW_ERROR, condición
        ;Actualiza la keyword de error
        ;UPDATE_KW KW_SPACE, condición
        ;Actualiza la keyword de espacio
        ;UPDATE_KW KW_MAYOR, condición
        ;Actualiza la keyword mayor
        ;UPDATE_KW KW_MENOR, condición
        ;Actualiza la keyword menor
        ;UPDATE_KW KW_NOT, condición
        ;Actualiza la keyword not
        ;UPDATE_KW KW_DIC, condición
        ;Actualiza la keyword dic
        ;UPDATE_KW KW_COMMENT, condición
        ;Actualiza la keyword comentario
        ;UPDATE_KW KW_COMILLA, condición
        ;Actualiza la keyword comillas
        ;UPDATE_KW KW_PUNTO, condición
        ;Actualiza la keyword punto
        ;UPDATE_KW KW_CORCHETE_CLOSE, condición
        ;Actualiza la keyword corchete fin
        ;UPDATE_KW KW_CORCHETE_OPEN, condición
        ;Actualiza la keyword corchete incio
        ;UPDATE_KW KW_COMILLAS, condición
        ;Actualiza la keyword comillas
        ;UPDATE_KW KW_EQUAL, condición
        ;Actualiza la keyword igual
        ;UPDATE_KW KW_SEMICOLON, condición
        ;Actualiza la keyword puntoycoma
        ;UPDATE_KW KW_POWER, condición
        ;Actualiza la keyword potencia
        ;UPDATE_KW KW_DIv, condición
        ;Actualiza la keyword división
        ;UPDATE_KW KW_MUL, condición
        ;Actualiza la keyword multiplicación
        ;UPDATE_KW KW_SUB, condición
        ;Actualiza la keyword resta
        ;UPDATE_KW KW_ADD, condición
        ;Actualiza la keyword suma
        ;UPDATE_KW KW_LLAVES_CLOSE, condición
        ;Actualiza la keyword llaves fin
        ;UPDATE_KW KW_LLAVES_OPEN, condición
        ;Actualiza la keyword llaves inicio
        ;UPDATE_KW KW_PARENTESIS_CLOSE, condición
        ;Actualiza la keyword paréntesis cerrar
        ;UPDATE_KW KW_COMMA, condición
        ;Actualiza la keyword coma
        ;UPDATE_KW KW_PARENTESIS_OPEN, condición
        ;Actualiza la keyword paréntesis abrir
        ;UPDATE_KW KW_CLASS, condición
        ;Actualiza la keyword clase
        ;UPDATE_KW KW_CTRL, condición
        ;Actualiza la keyword controlador
        ;UPDATE_KW KW_VAR, condición
        ;Actualiza la keyword variable
;



;Parser/Compiler/lexer
;Contexto VAR completo (falta mensaje)
    mov r9, 0 ;comienzo
    %macro FIRSTcond 1
    mov rdx, r15    ;Contexto
    shr rdx, %1     ;tipo KW
    and rdx, 1      ;Filtro and
    add r9, rdx     ;
    %endmacro
    %macro cond 1
    mov rdx, r15    ;Contexto activación
    shr rdx, %1     ;Tipo KW
    and rdx, 1      ;Filtro and
    and r9, rdx     ;Si es correcto sigue, sino anula
    %endmacro
    %macro elsecond 1
    mov rdx, r15        ;Acceder al contexto
    shr rdx, %1         ;Ubicación
    and rdx, 1          ;Filtro and
    xor r9, rdx         ;conexión inversa
    xor r9, 1           ;negación
    %endmacro
    %macro numero 1 ;número
    mov rdx, r15	;Mapa de contexto
    mov r8, r15		;Sistema de contexto emparejado
    shr r8, %1		;Detecta si es 1
    and r8, 1
    shr rdx, %1		;detecta si es 1
    and rdx, 1
    imul rdx, %1		;detecta valor
    sub rdx, 31 		;restar 31
    imul rdx, r8		;doble verificación
    ;Multiplicación x10
    imul rdx, r11
    div r11, 10			;El registro r11, acumula la multiplicación
    and rdx, 0x7FFF ;Limitar 15 bits
    or rdx, 0x8000  ;Bit de umbral (bit 16 = SIMD natural)
    add rbx, rdx    ;Añadir a rbx, el resultado de rdx
    %endmacro
    %macro desplazar
    cond KW_COMMA
    mov rdx, 1
    shl rdx, 4
    shl rbx, rdx;deja 16 lugares, para la próxima VAR
    %endmacro
    ;if["VAR"]
        FIRSTcond KW_VAR
        ;if(" ")
            cond KW_SPACE
            ;if["("]
                cond KW_PARENTESIS_OPEN
                ;if("umbral")
                numero KW_0         ;¿Es 0?
                UPDATE_KW KW_0      ;Actualizar 0
                numero KW_1         ;¿Es 9?
                UPDATE_KW KW_1      ;Actualizar 1
                numero KW_2         ;¿Es 8?
                UPDATE_KW KW_2      ;Actualizar 2
                numero KW_3         ;¿Es 7?
                UPDATE_KW KW_3      ;Actualizar 3
                numero KW_4         ;¿Es 6?
                UPDATE_KW KW_4      ;Actualizar 4
                numero KW_5         ;¿Es 5?
                UPDATE_KW KW_5      ;Actualizar 5
                numero KW_6         ;¿Es 4?
                UPDATE_KW KW_6      ;Actualizar 6
                numero KW_7         ;¿Es 3?
                UPDATE_KW KW_7      ;Actualizar 7
                numero KW_8         ;¿Es 2?
                UPDATE_KW KW_8      ;Actualizar 8
                numero KW_9         ;¿Es 1?
                UPDATE_KW KW_9      ;Actualizar 9
                ;if[","]
                    desplazar   ;Prepara para la siguiente variable
                        ;if[")"]
                            cond KW_PARENTESIS_CLOSE
                              ;if[","]
                                cond KW_COMMA
                                
        ;else("a-z,A-Z,0-9")
            elsecond KW_PARENTESIS_OPEN
            elsecond KW_SPACE
            detectar
            
    ;end
        mov r9, 0           ;reinicio contexto
;Contexto CTRL completo (falta dirección)
    ;if["CTRL"]
        FIRSTcond(KW_CTRL)
        ;if(" ")
            cond(KW_SPACE)
            ;if["{"]
                cond(KW_LLAVES_OPEN)
                ;if["1/0"]
                    cond(KW_0)
                    elsecond(KW_0)
                    ;if[","]
                        cond(KW_COMMA)
                            ;if["Destino"]
                            mov rdx, INPUT  ;Acceder al input actual
                            xor rax, rdx    ;Xorid 
                                ;if[" "]
                                cond(KW_SPACE)
                                cmovnz rax, ID_DIRECTION
                                    ;if["+"]
                                    cond(KW_ADD)
                                    ;do
                                    ;si + es correcto 
                                    ;else[!"+"]
                                    elsecond(KW_ADD)
                                    ;do
                                        ;if["-"]
                                        cond(KW_SUB)
                                        ;else[!"-"]
                                        elsecond(KW_SUB)
                                            ;if["*"]
                                            cond(KW_MUL)
                                            ;do
                                            ;else[!"*"]
                                            elsecond(KW_MUL)
                                            ;do
                                                ;if["**"]
                                                cond(KW_POWER)
                                                ;do                                    
                                                ;else[!"**"]
                                                elsecond(KW_POWER)
                                                ;do
                                                    ;if["/"]
                                                    cond(KW_DIV)
                                                    ;do
                                                    ;else[!"/"]
                                                    elsecond(KW_DIV)
                                                    ;do  
                            ;if["}"]
                                cond(KW_LLAVES_OPEN)
                                ;if[","]
                                    cond(KW_COMMA)
        ;else("a-z,A-Z,0-9")
            elsecond(KW_LLAVES_OPEN)
            mov rax, rdx    ;Iniciamos el acumulador
            shl rax, 9      ;1 byte + 1 bit
            sub rax, 1      ;restar 1 para que sea FF
            and rax, INPUT  ;ingresamos el byte
            xor rax, r13    ;xor index
            add r13, rax    ;añadir resultado de la xor
            shl r13, rcx    ;desplazar según contador
            add rcx, 1      ;aumentar contador en 1
    ;end
    mov r9, 0           ;reinicio contexto
;Contexto CLASS incompleto
    ;if["CLASS"]
        FIRSTcond(KW_CLASS)
        ;if[" "]
            cond(KW_SPACE)
            ;if["="]
                cond(KW_EQUAL)
                ;if[("("]
                    cond(KW_PARENTESIS_OPEN)
                    ;if["VAR"]
                        cond(KW_VAR)
                            
                    ;else["CTRL"]
                    elsecond(KW_VAR)
                        
    ;if[!" "]
        elsecond(KW_SPACE)
        shl rax, 9          ;1 byte + 1 bit
        sub rax, 1          ;restar 1 para que sea FF
        and rax, INPUT      ;ingresamos el byte
        xor rax, r13        ;xor index
        add r13, rax        ;añadir resultado de la xor
        shl r13, rcx        ;desplazar según contador
        add rcx, 1          ;aumentar contador en 1
    ;else[")"]
        cond(KW_PARENTESIS_CLOSE)
        ;end
        mov r9, 0       ;Reiniciar contexto
        ;if(";")
        mov rdx, r15        ;acceder al contexto
        shl rdx, 26         ;ubicación ;
        and rdx, 1          ;and
        mov r9, rdx         ;lectura agreado a r9
    ;end
