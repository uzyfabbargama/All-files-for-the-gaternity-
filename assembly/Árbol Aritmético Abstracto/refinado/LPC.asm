;SHL 0b10 = 1
;SHR 0b10 = 100
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
%define sys_write 4
%define out 1
%define insterrupcción_Linux 128
%define noop 0x27
%define end_program 1
%define good_ejec 0
%macro escribir(2) ;cond + VARMsg
    mov r9, %1 ;Tomar condición
    dec r9 ;r9 - 1, 1 → 0, 0 → -1
    not r9

    mov rax, sys_write
    mov rdi, out
    mov rsi, %2
    and rsi, r9
    mov rdx, %2.len
    and rdx, r9
    int 0x80
%endmacro
section .data
    msg db VARMsg, 10
    len equ $ - msg
section .text 
    global _start

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
;Definir 1
    %define KW_1 31 
    %define P_1 0x80000000
;Definir 2
    %define KW_2 32 
    %define P_2 0x100000000
;Definir 3
    %define KW_3 33 
    %define P_3 0x200000000
;Definir 4
    %define KW_4 34 
    %define P_4 0x400000000
;Definir 5
    %define KW_5 35 
    %define P_5 0x800000000
;Definir 6
    %define KW_6 36 
    %define P_6 0x1000000000
;Definir 7
    %define KW_7 37 
    %define P_7 0x2000000000
;Definir 8
    %define KW_8 38 
    %define P_8 0x4000000000
;Definir 9
    %define KW_9 39 
    %define P_9 0x8000000000
;Definir 0
    %define KW_0 40 
    %define P_0 0x10000000000
%macro parse_digito 0
xor rax, rax
%assign i 31
%rep 10
mov r9, r15
shr r9, i       ;mover bit i a posición 0
and r9, 1       ;aislar el bit
;Si r9=1, este es el dígito activo
mov r10, if
sub r10, 31     ;r10 = 0-9
add r10, 1      ;r10 = 1-10
cmp r10, 10     
cmove r10, 0    ;10 → 0

; Multiplicar por la máscara
imul r10, r9    ;r10 = valor si activo, 0 sino
add rax, r10    ;sumar al acumulador (solo uno será no-cero)

%assign i i+1
%endrep
;2. RAX ahora tiene el digito (0-9) o 0 si no era dígito
;Continuar con el parsing...
%endmacro
parse_umbral:
;procesar secuencia: (N → N → N)
xor rbx, rbx    ;Acumulador del umbral
mov rcx, 0      ;Contador de dígitos

.loop:
;1. Usar Macro cond para detectar digito
%assign i 31
%rep 10
    cond(i)
    ;Si recibe r9 = 1, procesar este dígito
    mov r8, i
    sub r8, 31
    add r8, 1
    cmp r8, 10
    cmove r8, 0

    ;Multiplicar por máscara
    imul r8, r9

    ;Acumular: rbx = (rbx << 4) | digito
    shl rbx, 4
    or rbx, r8
    
    ;Incrementar contador
    add rcx, r9

.not_this_digit:
    %assign i i+1
%endrep
;2: Verificar como (continuar) o paréntesis (fin)
;Usar cond(KW_COMMA) y cond(KW_PARENTESIS_CLOSE)

;¡SIN NINGÚN CMP explícito con caracteres ASCII! 
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
        super_ifVAR("V", "A", "R")
            ;do
            do ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        super_ifCTRL("C", "T", "R", "L")
            ;do
            do ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        super_ifCLASS("C", "L", "A", "S", "S")
            ;do
            do ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        if(P_PARENTESIS_OPEN,"(")
        cmovnz rax, r10 ;Operador
            ;do
            do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        if(P_COMMA, ",")
            ;do
            do ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        if(P_PARENTESIS_CLOSE, ")")
            ;do
            do;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        if(P_LLAVES_OPEN, "{")
            ;do
            do ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        if(P_LLAVES_CLOSE, "}")
        ;do
            do ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        if(P_ADD, "+")
        ;do
            do ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        if(P_SUB, "-")
            ;do
            do ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        if(P_MUL, "*")
            ;do
            do ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        if(P_DIV, "/")
            ;do
            do ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        super_ifPP("*", "*")
            ;do
            do;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        if(P_SEMICOLON, ";")
            ;do
            do ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
        ;if("=")
        if(P_EQUAL, "=")
            ;do
            do ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        if(P_COMILLAS,'"')
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
        ;if("[")
        if(P_CORCHETE_OPEN,"[")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
        ;if("]")
        if(P_CORCHETE_CLOSE, "]")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
        ;if('.')
        if(P_PUNTO, ".")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
        ;if("'")
            if(P_COMILLA, "'")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
        ;if("#")
            if(P_COMMENT, "#")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
        ;if(':')
            if(P_DIC, ":")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
        ;if('!')
            if(P_NOT, "!")
            ;do
            do ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
        ;if("<")
            if(P_MENOR, "<")
            ;do
            do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(">")
            if(P_MAYOR, ">")
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(" ")
            if(P_SPACE, " ")
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
		;if("e")
            if(P_ERROR, "e")
                ;do
                do ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if("\n" (10))
            if(P_NEW_LINE, 10)
            ;DO
            do
        ;if("^" (10))
            if(P_XOR, 10)
            ;DO
            do
        ;if("&" (10))
            if(P_AND, 10)
            ;DO
            do
        ;if("|" (10))
            if(P_OR, 10)
            ;DO
            do
        ;if("1" (10))
            if(P_1, 10)
            ;DO
            do
        ;if("2" (10))
            if(P_2, 10)
            ;DO
            do
        ;if("3" (10))
            if(P_3, 10)
            ;DO
            do
        ;if("4" (10))
            if(P_4, 10)
            ;DO
            do
        ;if("5" (10))
            if(P_5, 10)
            ;DO
            do
        ;if("6" (10))
            if(P_6, 10)
            ;DO
            do
        ;if("7" (10))
            if(P_7, 10)
            ;DO
            do
        ;if("8" (10))
            if(P_8, 10)
            ;DO
            do
        ;if("9" (10))
            if(P_9, 10)
            ;DO
            do
        ;if("0" (10))
            if(P_0, 10)
            ;DO
            do
        
;);

;Actualizar y comparar, mediante xor zf
    %define verdad
    %macro UPDATE_KW 1
        mov r9, r15      ;obtener el mapa completo
        xor r9, %1       ;Si es 0 no lo destruye, si es r15, si    
        sub cl, 1        ;Añadido 1bit al lector
        shl r9, cl       ;desplazado r9 lo que nos marca el lector
        and r9, 0x1      ;toma un solo bit
        xor r9, 1        ;compara si el slot es 1
        cmovz rax, verdad;compara la zf y lo mueve a rax
        shl rax, cl      ;aplica la máscara según el lector
        sub r15, rax     ;Reinicia estado de 1 → 0
    %endmacro

    ;CL = registro 8 bits de cantidad de bits
    ;CTRL condición[26]{0} 0
        UPDATE_KW r8
    ;CTRL condición[26]{0} 9
        UPDATE_KW r8    
    ;CTRL condición[26]{0} 8
        UPDATE_KW r8
    ;CTRL condición[26]{0} 7
        UPDATE_KW r8
    ;CTRL condición[26]{0} 6
        UPDATE_KW r8
    ;CTRL condición[26]{0} 5
        UPDATE_KW r8
    ;CTRL condición[26]{0} 4
        UPDATE_KW r8
    ;CTRL condición[26]{0} 3
        UPDATE_KW r8
    ;CTRL condición[26]{0} 2
        UPDATE_KW r8
    ;CTRL condición[26]{0} 1
        UPDATE_KW r8
    ;CTRL condición[26]{0} |
        UPDATE_KW r8
    ;CTRL condición[26]{0} &
        UPDATE_KW r8
    ;CTRL condición[26]{0} ^
        UPDATE_KW r8 
    ;CTRL condición[26]{0} \n
        UPDATE_KW r8 
    ;CTRL condición[26]{0} e
        UPDATE_KW r8
    ;CTRL condición[26]{0} " "
        UPDATE_KW r8
    ;CTRL condición[25]{0} ">"
        UPDATE_KW r8
    ;CTRL condición[24]{0} "<"
        UPDATE_KW r8
    ;;CTRL condición[23]{0} "!"
        UPDATE_KW r8
    ;;CTRL condición[22]{0} ":"
        UPDATE_KW r8
    ;;CTRL condiciónr[21]{0} "#"
        UPDATE_KW r8
    ;;CTRL condición[20](1) "'"
        UPDATE_KW r8
    ;;CTRL condiciónr[19]{0} "N"
        UPDATE_KW r8
    ;;CTRL condición[18]{0} "."
        UPDATE_KW r8
    ;;CTRL condiciónr[17]{0} "]"
        UPDATE_KW r8
    ;;CTRL condición[16]{0} "["
        UPDATE_KW r8
    ;;CTRL condiciónr[15]{0} '"'
        UPDATE_KW r8
    ;;CTRL condición[14]{0} "="
        UPDATE_KW r8
    ;CTRL separador[13]{0} ";"
        UPDATE_KW r8
    ;;CTRL condición[12]{0} "**"
        UPDATE_KW r8
    ;;CTRL condiciónr[11]{0} "/"
        UPDATE_KW r8
    ;;CTRL condición[10]{0} "*"
        UPDATE_KW r8
    ;;CTRL condiciónr[9]{0} "-"
        UPDATE_KW r8
    ;;CTRL condición[8]{0} "+"
        UPDATE_KW r8
    ;;CTRL condiciónr[7]{0} "}"
        UPDATE_KW r8
    ;;CTRL condición[6]{0} "{"
        UPDATE_KW r8
    ;;CTRL condiciónr[5]{0} ")"
        UPDATE_KW r8
    ;;CTRL condición[4]{0} ","
        UPDATE_KW r8
    ;;CTRL condiciónr[3]{0} "("
        UPDATE_KW r8
    ;;CTRL condición[2]{0} "CLASS"
        UPDATE_KW r8
    ;;CTRL condiciónr[1]{0} "CTRL"
        UPDATE_KW r8
    ;;CTRL condición[0]{0} "VAR"
        UPDATE_KW r8
;



;Parser/Compiler/lexer
;Contexto VAR completo (falta mensaje)
    mov r9, 0 ;comienzo
    %macro FIRSTcond (1)
    mov rdx, r15    ;Contexto
    shl rdx, %1     ;tipo KW
    and rdx, 1      ;Filtro and
    add r9, rdx     ;
    %endmacro
    %macro cond(1)
    mov rdx, r15    ;Contexto activación
    shl rdx, %1     ;Tipo KW
    and rdx, 1      ;Filtro and
    and r9, rdx     ;Si es correcto sigue, sino anula
    %endmacro
    %macro elsecond (1)
    mov rdx, r15        ;Acceder al contexto
    shl rdx, %1         ;Ubicación
    and rdx, 1          ;Filtro and
    xor r9, rdx         ;conexión inversa
    xor r9, 1           ;negación
    %endmacro
    ;if["VAR"]
        FIRSTcond(KW_VAR)
        ;if(" ")
            cond(KW_SPACE)
            ;if["("]
                cond(KW_PARENTESIS_OPEN)
                ;if("umbral")
                    mov rdx, r15         ;Registro de lectura
                    mov rax, 1          ;inicio umbral
                    mov rdx, 1          ;También inicio umbral
                    mov cl, 4           ;desplazador hexadecimal
                    shl rdx, cl          ;x16
                    and rdx, 0xF        ;Límite de 4 bits para el input
                    add rbx, rdx        ;Guardar dígito de umbral en RBX
                    shl rax, cl          ;se agrega el bit del umbral
                ;if[","]
                    mov rdx, 0      ;Reiniciar registro de lectura
                    cond(KW_COMMA)
                    xor rbx, r9     ;invierte los bits si hay una coma detectada
                    dec rbx         ;para complemento a 2
                        ;if[")"]
                            cond(KW_PARENTESIS_CLOSE)
                              ;if[","]
                                cond(KW_COMMA)
                                cmp r9, 1
                                cmovz r8, r15 ;Para reiniciar contexto
        ;else("a-z,A-Z,0-9")
            elsecond(KW_PARENTESIS_OPEN)
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
