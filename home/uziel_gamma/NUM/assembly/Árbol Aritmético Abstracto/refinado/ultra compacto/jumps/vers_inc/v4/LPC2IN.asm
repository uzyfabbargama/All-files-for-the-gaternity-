section .data
    INPUT db "VAR x (50)", 0x0a    ; código de entrada (10 = \n)

section .bss
    NameSpace: resb 0x800000        ; 8MB (sin guiones bajos en NASM)
    List: resb 0x100000             ; 1MB (lo descomento porque lo usas)

section .text
    global _start


;PE (propósito geneal)
;PE (propósito específico)
;registros temporales
    ;rax PG #comparación
    ;rcx PG #para el mul
    ;rdx PG #para guardar bytes
    ;rsi PE puntero de byte
    ;rdi PE dirección memoria
    ;r8 PG # Usado sólo en xif como temporal
    ;r9 PG #operador condicional
    ;r10 PG #segundo operando
    ;r11 PG #(xorid temporal)
;registros permanentes
    ;rbx PG para expansión
    ;rsp PE
    ;rbp PE
    ;r12 PG numeros
    ;r13 PG Puntero a Byte
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
%include "constans.inc"
%include "macros.inc"
_start:
    xor rsi, rsi
    xor r13, r13
    xor r9, r9      
    xor r8, r8      
    xor rax, rax    
    xor rcx, rcx    
    ;rdi = dirección de memoria
    ;rsi = puntero del byte
    xor r10, r10
    xor r11, r11
    xor r12, r12
    xor r14, r14
    xor r15, r15
    xor rbx, rbx
    jmp _Parser
_Parser:
    %include "parser.inc"
.comment:
    si KW_NEW_LINE, 10
        skip KW_NEW_LINE, r15
        test r9, r9
        mov rax, 0x000807F801FE7FC ;cargamos el monstruo
        and r15, rax ;0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 11111111 0 0 0 0 0 0 0 0 0 0 11111111 0 0 11111111 1 0 0
        ;Update: VAR CTRL , ) } + - * / ** ; = " ] . ' # : ! < >  \n ^ & | 0 1 2 3 4 5 6 7 8 9 0
        ;Estatic: CLASS ( { [ e
        jz .comment
        jnz _Factory
        ; Por ahora, matamos N-Lang al primer \n
        mov rax, 60         ; syscall exit
        xor rdi, rdi        ; código 0
        syscall
.numbers:
    capturar_numero r12
    mov r12, [List] ; Mover r12 a la lista
    jmp _Parser
.texto:
    expanse
    jmp .constructor
.constructor:
    mov r9, 0
    FIRSTcond KW_COMILLA, r15
        test r9, r9
        jnz _Parser
        mov rdx, [rbx] ; Movemos a la dirección que nos dió el kernel, el byte actual
    elsecond KW_COMILLAS, r15
        test r9, r9
        jnz _Parser
        mov rdx, [rbx]
        mov r9, 1
        suma_cond 1, r13
        inc r13
        jmp .constructor ; Siguiente byte
.operation:
    mov r11, [List] ;mover
    addcond KW_ADD, r10, r12
    subcond KW_SUB, r10, r12
    ;mulcond KW_MUL, r10, r12
    ;divcond KW_DIV, r10, r12
    orcond KW_OR, r10, r12
    xorcond KW_XOR, r10, r12
    andcond KW_AND, r10, r12
_Factory:
    FIRSTcond KW_VAR, r15
            cond KW_PARENTESIS_OPEN, r15
                cond KW_COMMA, r15
                    test r9, r9
                    jnz .vari
                    
                    ;Variable creada con éxito
    FIRSTcond KW_CTRL, r15
            cond KW_LLAVES_OPEN, r15
                test r9, r9
                jnz .ctrl
    FIRSTcond KW_CLASS, r15
        cond KW_PARENTESIS_OPEN, R15
            cond KW_PARENTESIS_CLOSE, R15
                cond KW_EQUAL, R15
                    cond KW_PARENTESIS_OPEN, R15
                            FIRSTcond KW_CTRL, r15
                                cond KW_LLAVES_OPEN, r15
                                    convert1b
                                    mov [NameSpace + r14 + 4], r12d
                    cond KW_COMMA, r15
                    cond KW_LLAVES_CLOSE, r15
                            cond KW_COMMA, r15
                                cond KW_PARENTESIS_CLOSE, R15
                                    cond KW_SEMICOLON, r15
.vari:
    mov [NameSpace + r14], r14d           ;se guarda el ID
    convert16b                      ; convertimos el valor de r12 
    mov [NameSpace + r14 + 4], r12d       ;Movemos el valor a la dirección de número
    cond KW_PARENTESIS_CLOSE, r15   ;detectamos que se cerró el paréntesis
    test r9, r9                     ;verificamos que r9 sea igual
    jnz _Parser                     ;saltamos al _Parser

.ctrl:
    mov [NameSpace + r14], r14d           ;Se guarda el ID
    convert1b                       ;Convertimos el valor de CTRL
    mov [NameSpace + r14 + 4], r12d       ;Movemos el valor de r12 a la dirección de memoria
    cond KW_COMMA, r15              ;verificamos la COMMA
    test r9, r9
    jnz .ctrl1
.ctrl1:
    ;mem_mov [NameSpace + r14 + 6], [List] ;saltamos el ID, el valor, y colocamos el destino
    cond KW_LLAVES_CLOSE, R15
    test r9, r9
    jnz _Parser                     ;Volvemos a la base
