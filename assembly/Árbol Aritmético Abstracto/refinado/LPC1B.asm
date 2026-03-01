;SHL 0b10 = 100
;SHR 0b10 = 1
;PE (propósito geneal)
;PE (propósito específico)
;registros temporales
    ;rax PG #comparación
    ;rcx PG #libre (usado CL)
    ;rdx PG #para guardar bytes
    ;rsi PE 
    ;rdi PE 
    ;r8 PG #libre
    ;r9 PG #operador
    ;r10 PG #libre
    ;r11 PG #libre
;registros permanentes
    ;rbx PG #para umbral
    ;rsp PE
    ;rbp PE
    ;r12 PG libre
    ;r13 PG para ID
    ;r14 PG libre
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
    ;10     ;"-"            ;Subkeyword sub
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
    %define P_CORCHETE_OPEN 0x10000
;Definir ]
    %define KW_CORCHETE_CLOSE 17
    %define P_CORCHETE_CLOSE 0x20000
;Definir .
    %define KW_PUNTO 18
    %define P_PUNTO 0x40000
;Definir '
    %define KW_COMILLA 19
    %define P_COMILLA 0x80000
;Definir #
    %define KW_COMMENT 20
    %define P_COMMENT 0x100000
;Definir :
    %define KW_DIC 21
    %define P_DIC 0x200000
;Definir !
    %define KW_NOT 22
    %define P_NOT 0x400000
;Definir <
    %define KW_MENOR 23
    %define P_MENOR 0x800000
;Definir >
    %define KW_MAYOR 24
    %define P_MAYOR 0x1000000
;Definir " "
    %define KW_SPACE 25
    %define P_SPACE 0x2000000
;Definir e
    %define KW_ERROR 26
    %define P_ERROR 0x4000000
;Definir \n (10 EN ASCII)
    %define KW_NEW_LINE 27 
    %define P_NEW_LINE 0x800000
;Definir ^
    %define KW_XOR 28
    %define P_XOR 0x10000000
;Definir &
    %define KW_AND 29
    %define P_AND 0x20000000
;Definir |
    %define KW_OR 30 
    %define P_OR 0x40000000
;Definir 0
    %define KW_0 31 
    %define P_0 0x80000000
;Definir 1
    %define KW_1 32 
    %define P_1 0x100000000
;Definir 2
    %define KW_2 33 
    %define P_2 0x200000000
;Definir 3
    %define KW_3 34 
    %define P_3 0x400000000
;Definir 4
    %define KW_4 35 
    %define P_4 0x800000000
;Definir 5
    %define KW_5 36 
    %define P_5 0x1000000000
;Definir 6
    %define KW_6 37 
    %define P_6 0x2000000000
;Definir 7
    %define KW_7 38 
    %define P_7 0x4000000000
;Definir 8
    %define KW_8 39 
    %define P_8 0x8000000000
;Definir 9
    %define KW_9 40 
    %define P_9 0x10000000000
_start:
;Parser[0]
    %macro super_ifVAR (3)
        mov rax, P_VAR     ;Resultado de Éxito
        mov r10, 0	        ;Registro de Fallo
    ;Check 'V'
        mov r9, INPUT[i]	;Cargar 'V'
        xor r9, %1     	;Si coincide, r9 = 0
        cmovnz r9, r10  	;Si no coincide (no zero), rax = (FALLA)
    ;Check 'A'
        mov r9, INPUT[i+1]  ;Cargar 'A'
        xor r9, %2     	;Si coincide, r9 = 0
        cmovnz rax, r10  	;Si no coincide (no zero), rax = (FALLA)
    ;Check 'R'
        mov r9, INPUT[i+2]  ;Cargar 'R'
        xor r9, %3     	;Si coincide, r9 = 0
        cmovnz rax, r10  	; Si falla (r9 != 0), rax = 0.
    %endmacro
    %macro super_ifCTRL (4)
            mov rax, P_CTRL     ;Resultado de Éxito
            mov r10, 0	        ;Registro de Fallo
            ;Check 'C'
            mov r9, INPUT[i] 	; Cargar 'C'
            xor r9, %1  	 	; Detectar byte
            cmovnz rax, r10  	; Si falla (r9 != 0), rax = 0.
            ;Check 'T'
            mov r9, INPUT[i+1]	; Cargar 'T'
            xor r9, %2			; Detectar byte
            cmovnz rax, r10		; Comparar byte
            ; Check 'R'
            mov r9, INPUT[i+2]	; Cargar 'R'
            xor r9, %3			; Detectar byte
            cmovnz rax, r10		; Comparar byte
            ; Check 'L'
            mov r9, INPUT[i+3]	; Cargar 'L'
            xor r9, %4			; Detectar byte
            cmovnz rax, r10		; Comparar byte
    %endmacro
    %macro super_ifCLASS (5)
            mov rax, P_CLASS    ;Resultado de éxito
            mov r10, 0          ;Registro de Fallo        
            ;Check C
            mov r9, INPUT[i]
            xor r9, %1
            cmovnz rax, r10
            ; Check L 
            mov r9, INPUT[i+1]
            xor r9, %2
            cmovnz rax, r10
            ; Check A 
            mov r9, INPUT[i+2]
            xor r9, %3
            cmovnz rax, r10
            ; Check S 
            mov r9, INPUT[i+3]
            xor r9, %4
            cmovnz rax, r10
            ; Check S
            mov r9, INPUT[i+4]
            xor r9, %5
            cmovnz rax, r10
    %endmacro
    %macro super_ifPP(2)   ;**
            mov rax, P_POWER
            mov r10, 0
            ; Check *
            mov r9, INPUT
            xor r9, %1
            cmovnz rax, r10
            ; Check *
            mov r9, INPUT[i+1]
            xor r9, %2
            cmovnz rax, r10
    %endmacro
    %macro if(2)
        mov rax, 0
        mov r10, %1         ;Para guardar
        mov r9, INPUT       ;Para comparar
        xor r9, %2          ;INPUT vs valor_real
        cmovnz rax, r10     ;
    %endmacro
    %macro do()
    add r12, rax
    ;nif_checker[0]
        ;if["VAR"]
        super_ifVAR "V", "A", "R"
            ;do
            do ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        super_ifCTRL "C", "T", "R", "L"
            ;do
            do ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        super_ifCLASS "C", "L", "A", "S", "S"
            ;do
            do ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        if P_PARENTESIS_OPEN,"("
        cmovnz rax, r10 ;Operador
            ;do
            do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        if P_COMMA, ","
            ;do
            do ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        if P_PARENTESIS_CLOSE, ")"
            ;do
            do;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        if P_LLAVES_OPEN, "{"
            ;do
            do ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        if P_LLAVES_CLOSE, "}"
        ;do
            do ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        if P_ADD, "+"
        ;do
            do ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        if P_SUB, "-"
            ;do
            do ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        if P_MUL, "*"
            ;do
            do ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        if P_DIV, "/"
            ;do
            do ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        super_ifPP "*", "*"
            ;do
            do;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        if P_SEMICOLON, ";"
            ;do
            do ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
        ;if("=")
        if P_EQUAL, "="
            ;do
            do ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        if P_COMILLAS,'"'
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
        ;if("[")
        if P_CORCHETE_OPEN,"["
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
        ;if("]")
        if P_CORCHETE_CLOSE, "]"
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
        ;if('.')
        if P_PUNTO, "."
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
        ;if("'")
            if P_COMILLA, "'"
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
        ;if("#")
            if P_COMMENT, "#"
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
        ;if(':')
            if P_DIC, ":"
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
        ;if('!')
            if P_NOT, "!"
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
        ;if("<")
            if P_MENOR, "<"
            ;do
            do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(">")
            if P_MAYOR, ">"
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(" ")
            if P_SPACE, " "
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
		;if("e")
            if P_ERROR, "e"
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if("\n" (10))
            if P_NEW_LINE, 10
            ;DO
            do
        ;if("^")
            if P_XOR, "^"
            ;DO
            do
        ;if("&" (10))
            if P_AND, "&"
            ;DO
            do
        ;if("|")
            if P_OR, "|"
            ;DO
            do
        ;if("1")
            if P_1, "1"
            ;DO
            do
        ;if("2")
            if P_2, "2"
            ;DO
            do
        ;if("3")
            if P_3, "3"
            ;DO
            do
        ;if("4")
            if P_4, "4"
            ;DO
            do
        ;if("5")
            if P_5, "5"
            ;DO
            do
        ;if("6")
            if P_6, "6"
            ;DO
            do
        ;if("7")
            if P_7, "7"
            ;DO
            do
        ;if("8")
            if P_8, "8"
            ;DO
            do
        ;if("9")
            if P_9, "9"
            ;DO
            do
        ;if("0")
            if P_0, "0"
            ;DO
            do
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
    %macro número 2 ;diez + r11
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
    mul r11, 10			;El registro r11, acumula los dieces
    imul rdx, r11
    and rdx, 0x7FFF ;Limitar 15 bits
    or rdx, 0x8000  ;Bit de umbral
    add rbx, rdx
    %endmacro
    %macro desplazar
    cond KW_COMMA
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
                número KW_0, 1     ;¿Es 0?
                UPDATE_KW KW_0  ;Actualizar 0
                número KW_1, 1     ;¿Es 9?
                UPDATE_KW KW_1  ;Actualizar 1
                número KW_2, 1      ;¿Es 8?
                UPDATE_KW KW_2  ;Actualizar 2
                número KW_3, 1     ;¿Es 7?
                UPDATE_KW KW_3  ;Actualizar 3
                número KW_4, 1     ;¿Es 6?
                UPDATE_KW KW_4  ;Actualizar 4
                número KW_5, 1     ;¿Es 5?
                UPDATE_KW KW_5  ;Actualizar 5
                número KW_6, 1     ;¿Es 4?
                UPDATE_KW KW_6  ;Actualizar 6
                número KW_7, 1     ;¿Es 3?
                UPDATE_KW KW_7  ;Actualizar 7
                número KW_8, 1     ;¿Es 2?
                UPDATE_KW KW_8  ;Actualizar 8
                número KW_9, 1     ;¿Es 1?
                UPDATE_KW KW_9  ;Actualizar 9
                ;if[","]
                    desplazar   ;Prepara para la siguiente variable
                        ;if[")"]
                            cond KW_PARENTESIS_CLOSE
                              ;if[","]
                                cond KW_COMMA
                                
        ;else("a-z,A-Z,0-9")
            elsecond KW_PARENTESIS_OPEN
            cmovz [tabla_IDs], r13 ;
            mov rax, rdx        ;Iniciamos el acumulador
            shl rax, 9          ;1 byte + 1 bit
            add rax, 255        ;sumar 255 para que sea FF
            and rax, INPUT      ;ingresamos el byte
            xor rax, r13        ;xor index
            add r13, rax        ;añadir resultado de la xor
            shl r13, rcx        ;desplazar según contador
            add rcx, 1          ;aumentar contador en 1
            
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
