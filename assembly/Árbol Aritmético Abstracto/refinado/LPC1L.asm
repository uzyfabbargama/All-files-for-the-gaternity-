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
    ;rdi PE dirección memoria
    ;r8 PG #usado con r9, para los números
    ;r9 PG #operador
    ;r10 PG #libre
    ;r11 PG #(xorid temporal)
;registros permanentes
    ;rbx PG #se une a R13, para guardar el umbral y valor de cada variable, (hasta 15 bits (de 0 a 15) por cada variable, para el valor, y un último bit para el umbral) = 4 variables por registro
    ;rsp PE
    ;rbp PE
    ;r12 PG valor umbrak
    ;r13 PG guarda números
    ;r14 PG xorid + rdi (dirección)
    ;r15 PG #contexto keywords 1-40 (total 61 bits (21 bits usados de contadores de 8 bits para paréntesis, corchetes y llaves))

;lista keywords
    ;1     ;"VAR"          ;Keyword: VAR
    ;2     ;"CTRL"         ;Keyword CTRL
    ;3     ;"CLASS"        ;Keyword CLASS
    ;4     ;"("            ;Subkeyword VAR-init (máximo 256 niveles de anidamiento)
    ;5     ;","            ;Subkeyword VAR-middle (depende de "(" para una extensión o ")" para un fin)
    ;6     ;")"            ;Subkeyword VAR-end (resta 1 al nivel sólo si hay al menos 1)
    ;7     ;"{"            ;Subkeyword CTRL-init (máximo 256 niveles de anidamiento)
    ;8     ;"}"            ;Subkeyword CTRL-end (depende la ",") (resta 1 al nivel sólo si hay al menos 1)
    ;9     ;"+"            ;Subkeyword add
    ;10     ;"-"           ;Subkeyword sub
    ;11    ;"*"            ;Subkeyword mul/shl
    ;12    ;"/"            ;Subkeyword div/shr
    ;13    ;"**"           ;Subkeyword power
    ;14    ;";"            ;Subkeyword end-CLASS
    ;15    ;"="            ;Subkeyword equal
    ;16    ;'"'            ;Subkeyword string1
    ;17 "["                 ;keyword lista e instancia (start) (máximo 256 niveles de anidamiento)
    ;18 "]"                 ;keyword lista e instancia (end) (depende la ",") (resta 1 al nivel sólo si hay al menos 1)
    ;19 "."                 ;keyword extension save/load
    ;20 "'"                 ;Subkeyword string2
    ;#" no hace falta, ya que la condición: hacer nada y/o ignorar es gratuita
    ;Error, el # no es simplemente "hacer nada" es "ignorar hasta recibir un salto de línea" 
    ;21 "#"                 ;Coemntarios
    ;22 ";"                 ;Otra Subekeyword de asignación y/o división
    ;23 "!"                 ;subkeyword para not
    ;24 "<"                 ;subkeyword para mayor qué (o load/save)
    ;25 ">"                 ;subkeyword para menor qué (o load/save)
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
    ; %1 = Bit a testear
	; %2 = Registro donde mirar (r15 para keywords, r8 para números)
    %macro FIRSTcond 2
    mov rdx, %2     ;Contexto
    shr rdx, %1     ;tipo KW
    and rdx, 1      ;Filtro and
    mov r9, rdx     ;Iniciar
    %endmacro
    ; %1 = Bit a testear
	; %2 = Registro donde mirar (r15 para keywords, r8 para números)
    %macro cond 2
    mov rdx, %2     ;Accedemos al registro que TÚ decidas
    shr rdx, %1     ;Movemos el bit al final
    and rdx, 1      ;Filtramos
    and r9, rdx     ;Cascada de éxito en r9
    %endmacro
    %macro elsecond 2
    mov rdx, %2         ;Acceder al contexto
    shr rdx, %1         ;Ubicación
    and rdx, 1          ;Filtro and
    xor r9, rdx         ;conexión inversa
    xor r9, 1           ;negación
    %endmacro
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
    %define P_PARENTESIS_OPEN 8 ;Dejamos 8 bits para contador de profundidad
;Definir ,
    %define KW_COMMA 11
    %define P_COMMA 0X800
;Definir )
    %define KW_PARENTESIS_CLOSE 12
    %define P_PARENTESIS_CLOSE 0X1000 ;Si recibe esto, reduce 1 al contador sólo si hay más que 1
;Definir {
    %define KW_LLAVES_OPEN 13
    %define P_LLAVES_OPEN 0x2000 ;dejamos 8 bits para contador de profundidad
;Definir }
    %define KW_LLAVES_CLOSE 21
    %define P_LLAVES_CLOSE 0x20_0000 ;Si recibe esto, reduce 1 al contador sólo si hay más que 1
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
    %define P_CORCHETE_OPEN 0x4000_0000 ;Dejamos 8 bits
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
    %define P_SPACE 0x2000_0000_00000
;Definir e
    %define KW_ERROR 47
    %define P_ERROR 0x4000_0000_00000
;Definir \n (10 EN ASCII)
    %define KW_NEW_LINE 48
    %define P_NEW_LINE 0x8000_0000_0000
;Definir ^
    %define KW_XOR 49
    %define P_XOR 0x100_0000_0000_0000
;Definir &
    %define KW_AND 50
    %define P_AND 0x200_0000_0000_0000
;Definir |
    %define KW_OR 51 
    %define P_OR 0x400_0000_0000_0000
;Definir 0
    %define KW_0 52 
    %define P_0 0x800_0000_0000_0000
;Definir 1
    %define KW_1 53 
    %define P_1 0x1000_0000_0000_0000
;Definir 2
    %define KW_2 54 
    %define P_2 0x2000_0000_0000_0000
;Definir 3
    %define KW_3 55 
    %define P_3 0x4000_0000_0000_0000
;Definir 4
    %define KW_4 56 
    %define P_4 0x8000_0000_0000_0000
;Definir 5
    %define KW_5 57 
    %define P_5 0x1000_0000_0000_0000
;Definir 6
    %define KW_6 58 
    %define P_6 0x2000_0000_0000_0000
;Definir 7
    %define KW_7 59 
    %define P_7 0x4000_0000_0000_0000
;Definir 8
    %define KW_8 60 
    %define P_8 0x8000_0000_0000_0000
;Definir 9
    %define KW_9 61 
    %define P_9 0x1_0000_0000_0000_0000



_start:
;Parser[0]
    %macro super_if2(2)   ;**
            mov rax, %2   ;Resultado éxito
            mov rdx, 0    ;Resultado fallo
            ; Check *
            mov r9b, INPUT
            shl r9, 8           ;Preparar para "*"
            ; Check *
            mov r9b, INPUT[rsi+1]
            xor r9, %1
            cmovnz rax, rdx
    %endmacro
    %macro super_if3 (1)
        mov rax, %2         ;Resultado de Éxito
        mov rdx, 0	        ;Registro de Fallo
    ;Check 'V'
        or r9b, INPUT[rsi]	    ;Cargar 'V'
        shl r9, 8           ;Preparar para "A"
    ;Check 'A'
        or r9b, INPUT[rsi+1]   ;Cargar 'A'
        shl r9, 8           ;Preparar para "R"
    ;Check 'R'
        or r9b, INPUT[rsi+2]   ;Cargar 'R'
        xor r9, %1     	;Si coincide, r9 = 0
        cmovnz rax, rdx  	; Si falla (r9 != 0), rax = 0.
    %endmacro
    %macro super_if4 (2)
            mov rax, %2          ;Resultado de Éxito
            mov rdx, 0	        ;Registro de Fallo
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
            cmovnz rax, rdx		; Comparar byte
    %endmacro
    %macro super_if5 (2)
            mov rax, %2         ;Resultado de éxito
            mov rdx, 0          ;Registro de Fallo        
            ;Check C
            mov r9b, INPUT[rsi]    ;Cargar "C"
            shl r9, 8           ;Preparar para "L"
            ; Check L 
            mov r9b, INPUT[rsi+1]
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
            cmovnz rax, rdx
    %endmacro
    %macro super_if6 (2) ;valor, Pos
            mov rax, %2        ;Resultado de éxito
            mov rdx, 0          ;Registro de Fallo        
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
            cmovnz rax, rdx
    %endmacro
    %macro super_if7 (2)
            mov rax, %2         ;Resultado de éxito
            mov rdx, 0          ;Registro de Fallo        
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
            cmovnz rax, rdx
    %endmacro
    %macro super_if8 (2)
            mov rax, %2         ;Resultado de éxito
            mov rdx, 0          ;Registro de Fallo        
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
            mov r9b, INPUT[rsi+ 3]
            shl r9, 8           ;Preparar para "5"
            ; Check 5
            mov r9b, INPUT[rsi+ 4]
            shl r9, 8           ;Preparar para "6"
            ; Check 6
            mov r9b, INPUT[rsi+ 5]
            shl r9, 8           ;Preparar para "7"
            ; Check 7
            mov r9b, INPUT[rsi+ 6]
            shl r9, 8           ;Preparar para "8"
            ; Check 8
            mov r9b, INPUT[rsi+ 7]
            xor r9, %1
            cmovnz rax, rdx
    %endmacro
    mov rdx, [INPUT]
    %macro if 2 			;destino, valor
        mov r9, rdx         ;Para comparar
        xor r9, %2          ;INPUT vs valor_real
        setz r9b            ;si era 0 le da 1
        shl r9, %1          ;desplazamos (si es 0 seguirá siendo 0, sino, será la máscara)
        or rax, r9          ;le agregamos rax
    %endmacro
    %macro do_in 1
    xor %1, rax
    %endmacro
    ;Number List
        ;1
        %define Num_0 0
        ;2
        %define Num_1 1
        ;3
        %define Num_2 2
        ;4
        %define Num_3 3
        ;5
        %define Num_4 4
        ;6
        %define Num_5 5
        ;7
        %define Num_6 6
        ;8
        %define Num_7 7
        ;9
        %define Num_8 8
        ;10
        %define Num_9 9
        ;11
        %define Num_10 10
        ;12
        %define Num_11 11
        ;13
        %define Num_12 12
        ;14
        %define Num_13 13
        ;15
        %define Num_14 14
        ;16
        %define Num_15 15
        ;17
        %define Num_16 16
        ;18
        %define Num_17 17
        ;19
        %define Num_18 18
        ;20
        %define Num_19 19
        ;21
        %define Num_20 20
        ;22
        %define Num_21 21
        ;23
        %define Num_22 22
        ;24
        %define Num_23 23
        ;25
        %define Num_24 24
        ;26
        %define Num_25 25
        ;27
        %define Num_26 26
        ;28
        %define Num_27 27
        ;29
        %define Num_28 28
        ;30
        %define Num_29 29
        ;31
        %define Num_30 30
        ;32
        %define Num_31 31
        ;33
        %define Num_32 32
        ;34
        %define Num_33 33
        ;35
        %define Num_34 34
        ;36
        %define Num_35 35
        ;37
        %define Num_36 36
        ;38
        %define Num_37 37
        ;39
        %define Num_38 38
        ;40
        %define Num_39 39
        ;41
        %define Num_40 40
        ;42
        %define Num_41 41
        ;43
        %define Num_42 42
        ;44
        %define Num_43 43
        ;45
        %define Num_44 44
        ;46
        %define Num_45 45
        ;47
        %define Num_46 46
        ;48
        %define Num_47 47
        ;49
        %define Num_48 48
        ;50
        %define Num_49 49
        ;51
        %define Num_50 50
        ;52
        %define Num_51 51
        ;53
        %define Num_52 52
        ;54
        %define Num_53 53

        ;55
        %define Num_54 54

        ;56
        %define Num_55 55

        ;57
        %define Num_56 56

        ;58
        %define Num_57 57

        ;59
        %define Num_58 58

        ;60
        %define Num_59 59

        ;61
        %define Num_60 60

        ;62
        %define Num_61 61

        ;63
        %define Num_62 62

        ;64
        %define Num_63 63

    ;num checker
        %macro if_num 2     ;byte, destino
        if %2, %1, %3
        do_in r13
        %endmacro
        
        %macro is_0 3       ;byte. destino, página
        if %2, %1           ;dato a comparar (cambia r9 si era 0 o 1)
        mov r8, r13         ;tomamos el historial de activaciones completo
        shr r8, %3          ;tomamos la página de dígitos
        and r8, 0x1FF       ;(0001 1111 1111) toma los 9 bits de pasado, y se fija si al menos hay 1
        setnz r8b			;verificar si no era 0
        and r8, 0x1        ;se filtra un sólo bit de r8
        and r9, r8          ;si y sólo si, r9 y r8, son 1, r9 es 1
        shl r9 %2           ;desplazar r9, al destino
        or r13, r9          ;enviar un bit al registro principal
        %endmacro
        %macro sumar_indice 0
        add rsi, r9         ;agregar 1 a RSI, sólo si r9 es 1
        %endmacro
%macro mul_10 0
    ; Supongamos que r9 es 1 (éxito) o 0 (nada)
    
    ; --- PREPARAR EL X8 ---
    mov cl, r9b        ; cl = 1 o 0
    lea rcx, [rcx * 2 + rcx] ; cl = 3 (si era 1) o 0 (si era 0)
    ; Ahora cl vale 3 o 0. Magia de LEA.
    
    mov ax, r12w       ; Copiamos r12
    shl ax, cl         ; Si cl=3 -> ax = r12 * 8. Si cl=0 -> ax = r12.
    
    ; --- PREPARAR EL X2 ---
    mov cl, r9b        ; cl = 1 o 0
    shl r12w, cl       ; Si cl=1 -> r12 = r12 * 2. Si cl=0 -> r12 = r12.
    
    ; --- EL COLAPSO ---
    ; Aquí hay un detalle: si r9 era 0, ax=r12 y r12=r12. 
    ; Si los sumas, r12 se duplica aunque no quieras.
    ; Necesitamos que AX sea 0 si r9 es 0.
    
    neg r9             ; r9 = 0xFFFF... (si era 1) o 0 (si era 0)
    and ax, r9w        ; Si r9 era 0, ax se vuelve 0.
    
    add r12w, ax       ; r12 = (r12*2) + (r12*8)  O  r12 = r12 + 0
%endmacro        
%macro suma_cond 1
	mov rdx, 0			; Limpiamos
    mov rdx, r9         ; Copiamos el éxito (0 o 1) a rdx
    neg rdx             ; rdx = 0 o FFFFFFFFFFFFFFFF
    and rdx, %1         ; rdx = 0 o VALOR
    add r12, rdx        ; ¡Inyección segura! r9 sigue vivo para el siguiente if
%endmacro
;num_checker
            if_num "1", Num_0
            sumar_indice
            FIRSTcond Num_0, r13
            suma_cond 1
            if_num "2", Num_1
            sumar_indice
            FIRSTcond Num_1, r13
            suma_cond 2
            if_num "3", Num_2
            sumar_indice
            FIRSTcond Num_2, r13
            suma_cond 3
            if_num "4", Num_3
            sumar_indice
            FIRSTcond Num_3, r13
            suma_cond 4
            if_num "5", Num_4
            sumar_indice
            FIRSTcond Num_4, r13
            suma_cond 5
            if_num "6", Num_5
            sumar_indice
            FIRSTcond Num_5, r13
            suma_cond 6
            if_num "7", Num_6
            sumar_indice
            FIRSTcond Num_6, r13
            suma_cond 7
            if_num "8", Num_7
            sumar_indice
            FIRSTcond Num_8, r13
            suma_cond 8
            if_num "9", Num_8
            sumar_indice
            FIRSTcond Num_8, r13
            suma_cond 9
            is_0 "0", Num_9, 0
            mul_10
            ;sig cifra
            sumar_indice
            if_num "1", Num_10
            sumar_indice
            FIRSTcond Num_10, r13
            suma_cond 1
            if_num "2", Num_11
            sumar_indice
            FIRSTcond Num_11, r13
            suma_cond 2
            if_num "3", Num_12
            sumar_indice
            FIRSTcond Num_12, r13
            suma_cond 3
            if_num "4", Num_13
            sumar_indice
            FIRSTcond Num_13, r13
            suma_cond 4
            if_num "5", Num_14
            sumar_indice
            FIRSTcond Num_14, r13
            suma_cond 5
            if_num "6", Num_15
            sumar_indice
            FIRSTcond Num_15, r13
            suma_cond 6
            if_num "7", Num_16
            sumar_indice
            FIRSTcond Num_16, r13
            suma_cond 7
            if_num "8", Num_17
            sumar_indice
            FIRSTcond Num_17, r13
            suma_cond 8
            if_num "9", Num_18
            sumar_indice
            FIRSTcond Num_18, r13
            suma_cond 9
            is_0 "0", Num_19, 10
            sumar_indice
            mul_10
            ;sig cifra
            if_num "1", Num_20
            sumar_indice
            FIRSTcond Num_20, r13
            suma_cond 1
            if_num "2", Num_21
            sumar_indice
            FIRSTcond Num_21, r13
            suma_cond 2
            if_num "3", Num_22
            sumar_indice
            FIRSTcond Num_22, r13
            suma_cond 3
            if_num "4", Num_23
            sumar_indice
            FIRSTcond Num_23, r13
            suma_cond 4
            if_num "5", Num_24
            sumar_indice
            FIRSTcond Num_24, r13
            suma_cond 5
            if_num "6", Num_25
            sumar_indice
            FIRSTcond Num_25, r13
            suma_cond 6
            if_num "7", Num_26
            sumar_indice
            FIRSTcond Num_26, r13
            suma_cond 7
            if_num "8", Num_27
            sumar_indice
            FIRSTcond Num_27, r13
            suma_cond 8
            if_num "9", Num_28
            sumar_indice
            FIRSTcond Num_28, r13
            suma_cond 9
            is_0 "0", Num_29, 20
            sumar_indice
            mul_10
            ;sig cifra
            if_num "1", Num_30
            sumar_indice
            FIRSTcond Num_30, r13
            suma_cond 1
            if_num "2", Num_31
            sumar_indice
            FIRSTcond Num_31, r13
            suma_cond 2
            if_num "3", Num_32
            sumar_indice
            FIRSTcond Num_32, r13
            suma_cond 3
            if_num "4", Num_34
            sumar_indice
            FIRSTcond Num_33, r13
            suma_cond 4
            if_num "5", Num_34
            sumar_indice
            FIRSTcond Num_34, r13
            suma_cond 5
            if_num "6", Num_35
            sumar_indice
            FIRSTcond Num_35, r13
            suma_cond 6
            if_num "7", Num_36
            sumar_indice
            FIRSTcond Num_36, r13
            suma_cond 7
            if_num "8", Num_37
            sumar_indice
            FIRSTcond Num_37, r13
            suma_cond 8
            if_num "9", Num_38
            sumar_indice
            FIRSTcond Num_38, r13
            suma_cond 9
            is_0 "0", Num_39, 30
            sumar_indice
            mul_10
            ;sig cifra
            if_num "1", Num_40
            sumar_indice
            FIRSTcond Num_40, r13
            suma_cond 1
            if_num "2", Num_41
            sumar_indice
            FIRSTcond Num_41, r13
            suma_cond 2
            if_num "3", Num_42
            sumar_indice
            FIRSTcond Num_42, r13
            suma_cond 3
            if_num "4", Num_43
            sumar_indice
            FIRSTcond Num_43, r13
            suma_cond 4
            if_num "5", Num_44
            sumar_indice
            FIRSTcond Num_44, r13
            suma_cond 5
            if_num "6", Num_45
            sumar_indice
            FIRSTcond Num_45, r13
            suma_cond 6
            if_num "7", Num_46
            sumar_indice
            FIRSTcond Num_46, r13
            suma_cond 7
            if_num "8", Num_47
            sumar_indice
            FIRSTcond Num_47, r13
            suma_cond 8
            if_num "9", Num_48
            sumar_indice
            FIRSTcond Num_48, r13
            suma_cond 9
            is_0 "0", Num_49, 40
            mul_10
            ;sig cifra
            if_num "1", Num_50
            sumar_indice
            FIRSTcond Num_50, r13
            suma_cond 1
            if_num "2", Num_51
            sumar_indice
            FIRSTcond Num_51, r13
            suma_cond 2
            if_num "3", Num_52
            sumar_indice
            FIRSTcond Num_52, r13
            suma_cond 3
            if_num "4", Num_53
            sumar_indice
            FIRSTcond Num_53, r13
            suma_cond 4
            if_num "5", Num_54
            sumar_indice
            FIRSTcond Num_54, r13
            suma_cond 5
            if_num "6", Num_55
            sumar_indice
            FIRSTcond Num_55, r13
            suma_cond 6
            if_num "7", Num_56
            sumar_indice
            FIRSTcond Num_56, r13
            suma_cond 7
            if_num "8", Num_57
            sumar_indice
            FIRSTcond Num_57, r13
            suma_cond 8
            if_num "9", Num_58
            sumar_indice
            FIRSTcond Num_58, r13
            suma_cond 9
            is_0 "0", Num_59, 50
            sumar_indice
            mul_10
            ;sig cifra
    
    %macro xorid 0
    add r9, 0xFFFFFFFFFFFFFFFF  ;1 = 0, 0 = FFFFFFFFFFFFFFFF
    and r11, r9     ;si r9 es 1, r11 desaparece, si es 0, no
    xor r11, input  ;se aplica la fórmula: id = id xor byte[i] << 1
    add r9, 2       ;FFFFFFFFFFFFFFFF = 1, 0 = 0b10
    and r9, 1       ;1 = 1, 0b10 = 0
    shl r11, r9     ;depende r9
    %endmacro
    %macro save 0
    mov r14, r11
    %endmacro
    ;nif_checker[0]
        ;if["VAR"]
        super_if3 ("VAR", P_VAR)
            ;do
            do_in r15;CTRL[0] {1, nif[0]((VAR[0]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
            xorid     ;si recibe 1, elimina el xorid (porque está en modo keyword/token) si recibe 0 empieza a guardar los datos basura (hasta el espacio o hasta detectar un token) (modo nombre)
            save      ;guarda el estado actual del xorid
        ;if["CTRL"]
        super_if4 ("CTRL", P_CTRL)
            ;do
            do_in r15;CTRL[1] {1, nif[0]((VAR[1]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CLASS"]
        super_if5 ("CLASS", P_CLASS)
            ;do
            do_in r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("(")
        if KW_PARENTESIS_OPEN,"("
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(",")
        if KW_COMMA, ","
            ;do
            do_in r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(")")
        if KW_PARENTESIS_CLOSE, ")"
            ;do
            do_in r15;CTRL[5] {1, nif[0]((VAR[5]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("{")
        if KW_LLAVES_OPEN, "{"
            ;do
            do_in r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("}")
        if KW_LLAVES_CLOSE, "}"
        ;do
            do_in r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("+")
        if KW_ADD, "+"
        ;do
            do_in r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("-")
        if KW_SUB, "-"
            ;do
            do_in r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("*")
        if KW_MUL, "*"
            ;do
            do_in r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("/")
        if KW_DIV, "/"
            ;do
            do_in r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("**")
        super_if2 ("**", P_POWER)
            ;do
            do_in r15;CTRL[12] {1, nif[0]((VAR[12]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(";")
        if KW_SEMICOLON, ";"
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("=")
        if KW_EQUAL, "="
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('"')
        if KW_COMILLAS,'"'
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("[")
        if KW_CORCHETE_OPEN,"["
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("]")
        if KW_CORCHETE_CLOSE, "]"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('.')
        if KW_PUNTO, "."
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("'")
            if KW_COMILLA, "'"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("#")
            if KW_COMMENT, "#"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(':')
            if KW_DIC, ":"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('!')
            if KW_NOT, "!"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("<")
            if KW_MENOR, "<"
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(">")
            if KW_MAYOR, ">"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(" ")
            if KW_SPACE, " "
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
		;if("e")
            if KW_ERROR, "e"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("\n" (10))
            if KW_NEW_LINE, 10
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("^")
            if KW_XOR, "^"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("&" (10))
            if KW_AND, "&"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("|")
            if KW_OR, "|"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("1")
            if KW_1, "1"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("2")
            if KW_2, "2"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("3")
            if KW_3, "3"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("4")
            if KW_4, "4"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("5")
            if KW_5, "5"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("6")
            if KW_6, "6"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("7")
            if KW_7, "7"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("8")
            if KW_8, "8"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("9")
            if KW_9, "9"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("0")
            if KW_0, "0"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
;);
    ;nif_checker[1]
        ;if["VAR"]
        super_if3 ("VAR", P_VAR)
            ;do
            do_in r15;CTRL[0] {1, nif[0]((VAR[0]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CTRL"]
        super_if4 ("CTRL", P_CTRL)
            ;do
            do_in r15;CTRL[1] {1, nif[0]((VAR[1]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CLASS"]
        super_if5 ("CLASS", P_CLASS)
            ;do
            do_in r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("(")
        if KW_PARENTESIS_OPEN,"("
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(",")
        if KW_COMMA, ","
            ;do
            do_in r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(")")
        if KW_PARENTESIS_CLOSE, ")"
            ;do
            do_in r15;CTRL[5] {1, nif[0]((VAR[5]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("{")
        if KW_LLAVES_OPEN, "{"
            ;do
            do_in r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("}")
        if KW_LLAVES_CLOSE, "}"
        ;do
            do_in r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("+")
        if KW_ADD, "+"
        ;do
            do_in r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("-")
        if KW_SUB, "-"
            ;do
            do_in r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("*")
        if KW_MUL, "*"
            ;do
            do_in r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("/")
        if KW_DIV, "/"
            ;do
            do_in r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("**")
        super_if2 ("**", P_POWER)
            ;do
            do_in r15;CTRL[12] {1, nif[0]((VAR[12]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(";")
        if KW_SEMICOLON, ";"
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("=")
        if KW_EQUAL, "="
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('"')
        if KW_COMILLAS,'"'
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("[")
        if KW_CORCHETE_OPEN,"["
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("]")
        if KW_CORCHETE_CLOSE, "]"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('.')
        if KW_PUNTO, "."
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("'")
            if KW_COMILLA, "'"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("#")
            if KW_COMMENT, "#"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(':')
            if KW_DIC, ":"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('!')
            if KW_NOT, "!"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("<")
            if KW_MENOR, "<"
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(">")
            if KW_MAYOR, ">"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(" ")
            if KW_SPACE, " "
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
		;if("e")
            if KW_ERROR, "e"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("\n" (10))
            if KW_NEW_LINE, 10
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("^")
            if KW_XOR, "^"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("&" (10))
            if KW_AND, "&"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("|")
            if KW_OR, "|"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("1")
            if KW_1, "1"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("2")
            if KW_2, "2"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("3")
            if KW_3, "3"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("4")
            if KW_4, "4"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("5")
            if KW_5, "5"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("6")
            if KW_6, "6"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("7")
            if KW_7, "7"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("8")
            if KW_8, "8"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("9")
            if KW_9, "9"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("0")
            if KW_0, "0"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
;);
    ;nif_checker[2]
        ;if["VAR"]
        super_if3 ("VAR", P_VAR)
            ;do
            do_in r15;CTRL[0] {1, nif[0]((VAR[0]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CTRL"]
        super_if4 ("CTRL", P_CTRL)
            ;do
            do_in r15;CTRL[1] {1, nif[0]((VAR[1]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CLASS"]
        super_if5 ("CLASS", P_CLASS)
            ;do
            do_in r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("(")
        if KW_PARENTESIS_OPEN,"("
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(",")
        if KW_COMMA, ","
            ;do
            do_in r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(")")
        if KW_PARENTESIS_CLOSE, ")"
            ;do
            do_in r15;CTRL[5] {1, nif[0]((VAR[5]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("{")
        if KW_LLAVES_OPEN, "{"
            ;do
            do_in r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("}")
        if KW_LLAVES_CLOSE, "}"
        ;do
            do_in r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("+")
        if KW_ADD, "+"
        ;do
            do_in r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("-")
        if KW_SUB, "-"
            ;do
            do_in r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("*")
        if KW_MUL, "*"
            ;do
            do_in r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("/")
        if KW_DIV, "/"
            ;do
            do_in r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("**")
        super_if2 ("**", P_POWER)
            ;do
            do_in r15;CTRL[12] {1, nif[0]((VAR[12]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(";")
        if KW_SEMICOLON, ";"
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("=")
        if KW_EQUAL, "="
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('"')
        if KW_COMILLAS,'"'
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("[")
        if KW_CORCHETE_OPEN,"["
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("]")
        if KW_CORCHETE_CLOSE, "]"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('.')
        if KW_PUNTO, "."
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("'")
            if KW_COMILLA, "'"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("#")
            if KW_COMMENT, "#"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(':')
            if KW_DIC, ":"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('!')
            if KW_NOT, "!"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("<")
            if KW_MENOR, "<"
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(">")
            if KW_MAYOR, ">"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(" ")
            if KW_SPACE, " "
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
		;if("e")
            if KW_ERROR, "e"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("\n" (10))
            if KW_NEW_LINE, 10
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("^")
            if KW_XOR, "^"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("&" (10))
            if KW_AND, "&"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("|")
            if KW_OR, "|"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("1")
            if KW_1, "1"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("2")
            if KW_2, "2"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("3")
            if KW_3, "3"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("4")
            if KW_4, "4"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("5")
            if KW_5, "5"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("6")
            if KW_6, "6"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("7")
            if KW_7, "7"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("8")
            if KW_8, "8"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("9")
            if KW_9, "9"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("0")
            if KW_0, "0"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
;);
    ;nif_checker[3]
        ;if["VAR"]
        super_if3 ("VAR", P_VAR)
            ;do
            do_in r15;CTRL[0] {1, nif[0]((VAR[0]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CTRL"]
        super_if4 ("CTRL", P_CTRL)
            ;do
            do_in r15;CTRL[1] {1, nif[0]((VAR[1]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if["CLASS"]
        super_if5 ("CLASS", P_CLASS)
            ;do
            do_in r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("(")
        if KW_PARENTESIS_OPEN,"("
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(",")
        if KW_COMMA, ","
            ;do
            do_in r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(")")
        if KW_PARENTESIS_CLOSE, ")"
            ;do
            do_in r15;CTRL[5] {1, nif[0]((VAR[5]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("{")
        if KW_LLAVES_OPEN, "{"
            ;do
            do_in r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("}")
        if KW_LLAVES_CLOSE, "}"
        ;do
            do_in r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("+")
        if KW_ADD, "+"
        ;do
            do_in r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("-")
        if KW_SUB, "-"
            ;do
            do_in r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("*")
        if KW_MUL, "*"
            ;do
            do_in r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("/")
        if KW_DIV, "/"
            ;do
            do_in r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("**")
        super_if2 ("**", P_POWER)
            ;do
            do_in r15;CTRL[12] {1, nif[0]((VAR[12]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(";")
        if KW_SEMICOLON, ";"
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("=")
        if KW_EQUAL, "="
            ;do
            do_in r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('"')
        if KW_COMILLAS,'"'
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("[")
        if KW_CORCHETE_OPEN,"["
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("]")
        if KW_CORCHETE_CLOSE, "]"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('.')
        if KW_PUNTO, "."
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("'")
            if KW_COMILLA, "'"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("#")
            if KW_COMMENT, "#"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(':')
            if KW_DIC, ":"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if('!')
            if KW_NOT, "!"
            ;do
            do_in r15 ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("<")
            if KW_MENOR, "<"
            ;do
            do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(">")
            if KW_MAYOR, ">"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if(" ")
            if KW_SPACE, " "
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
		;if("e")
            if KW_ERROR, "e"
                ;do
                do_in r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
                if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("\n" (10))
            if KW_NEW_LINE, 10
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("^")
            if KW_XOR, "^"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("&" (10))
            if KW_AND, "&"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("|")
            if KW_OR, "|"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("1")
            if KW_1, "1"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("2")
            if KW_2, "2"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("3")
            if KW_3, "3"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("4")
            if KW_4, "4"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("5")
            if KW_5, "5"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("6")
            if KW_6, "6"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("7")
            if KW_7, "7"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("8")
            if KW_8, "8"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("9")
            if KW_9, "9"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
        ;if("0")
            if KW_0, "0"
            ;DO
            do_in r15
            if 1, " " ;le suma 1, si se detecta espacio
            do_in rsi ;recibe 1 para saltear el espacio
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
                xor r12, 0xFFFF ;registro del umbral, filtrado por 16 bits
                add r12, 1      ;para el complemento a 2
                ;if[","]
                    cond KW_COMMA
                    add rbx, r12 ;guardar
                    shl rbx, 16  ;dejar lugar a otra variable
                        ;if[")"]
                            cond KW_PARENTESIS_CLOSE
                              ;if[","]
                                cond KW_COMMA
            
    ;end
        mov r9, 0           ;reinicio contexto
;Contexto CTRL completo (falta dirección)
    ;if["CTRL"]
        FIRSTcond KW_CTRL
        ;if(" ")
            cond KW_SPACE
            ;if["{"]
                cond KW_LLAVES_OPEN
                ;if["1/0"]
                    cond KW_0
                    shl r9, 15      ;1 = 2¹⁶, 0 = 0
                    mov r10, 0b0111111111111111
                    or r10, r9 ;1 = FFFF, 0 = 7FFF                    
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
        elsecond(KW_SPACE), r15
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
