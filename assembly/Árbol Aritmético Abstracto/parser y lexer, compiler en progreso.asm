;PE (propósito geneal)
;PE (propósito específico)
;registros temporales
    ;rax PG #comparación
    ;rcx PG #libre (usado CL)
    ;rdx PG #para guardar bytes
    ;rsi PE 
    ;rdi PE 
    ;r8 PG #contador de bits temporal (prácticamente libre)
    ;r9 PG #operador
    ;r10 PG #libre
    ;r11 PG #libre
;registros permanentes
    ;rbx PG #para umbral
    ;rsp PE
    ;rbp PE
    ;r12 PG #CLASS keywords 1-27
    ;r13 PG para ID
    ;r14 PG libre
    ;r15 PG #contexto keywords 1-27
_start:
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
    ;20 "N"                 ;keyword extension N-Lang
    ;21 "'"                 ;Subkeyword string2
    ;#" no hace falta, ya que la condición: hacer nada y/o ignorar es gratuita
    ;Error, el # no es simplemente "hacer nada" es "ignorar hasta recibir un salto de línea" 
    ;22 "#"                 ;Coemntarios
    ;23 ";"                 ;Otra Subekeyword de asignación y/o división
    ;24 "!"                 ;subkeyword para not
    ;25 "<"                 ;subkeyword para mayor qué
    ;26 ">"                 ;subkeyword para menor qué
    ;27 " "                 ;subkeyword para delimitar variables
    ;28 "e"					;subkeyword para errores
;nif[0](16) = CLASS nif = (
    mov cl, 0      ;contador de bits
    mov r12, 0       ;clase principal nif(1)
    ;CTRL condición[0](1) "VAR"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[1]{0} "CTRL" 
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[2](1) "CLASS"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[3]{0} "("
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[4](1) ","
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[5]{0} "(" 
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
    ;CTRL condición[6](1) "}"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[7]{0} "{"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[8](1) "+"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[9]{0} "-"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[10](1) "*"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[11]{0} "/"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[12](1) "**"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[13]{0} ";"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[14](1) "="
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condiciónr[15]{0} '"'
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[16](1) "["
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[17]{0} ']'
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[18](1) "."
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[19]{0} "nlang"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[20](1) "'"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[21]{0} "#"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[22](1) ":"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (11)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[23]{0} "!"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[24](0) "<"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (11)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[25](0) ">"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (11)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[26](0) " "
        mov r9, 1       ;registro de operación
        add cl, 2       ;añadido 2 bits al lector
        shl r9, cl      ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[27](0) "e"
        mov r9, 1       ;registro de operación
        add cl, 2       ;añadido 2 bits al lector
        shl r9, cl      ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r12, r9     ;añadido a la CLASS
;);
;Actualizar y comparar, mediante cmp zf
    ;CL = cantidad de bits
        ;CTRL condición[27]{0} "e"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1     ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10   ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)

    ;CTRL condición[26]{0} " "
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1     ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10   ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;CTRL condición[25]{0} ">"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10   ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;CTRL condición[24](1) "<"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto ";" borra contexto de otras keywords y subkeywords
    ;;CTRL condición[23]{0} "!"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10   ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[22](1) ":"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto ";" borra contexto de otras keywords y subkeywords
    ;;CTRL condiciónr[21]{0} "#"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[20](1) "'"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "**" para detectar exponente
    ;;CTRL condiciónr[19]{0} "N"
        mov r9, r12      ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[18](1) "."
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "/" para detectar divisor
    ;;CTRL condiciónr[17]{0} "]"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[16](1) "["
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "*" para detectar factor
    ;;CTRL condiciónr[15]{0} '"'
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[14](1) "="
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "-" para detectar substraendo
    ;CTRL separador[13]{0} ";"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante      
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[12](1) "**"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "+" para detectar sumando
    ;;CTRL condiciónr[11]{0} "/"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[10](1) "*"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "}" cierre de CTRL
    ;;CTRL condiciónr[9]{0} "-"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[8](1) "+"
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a r1ax(para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "{" abrir CTRL
    ;;CTRL condiciónr[7]{0} "}"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[6](1) "{"
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto ")" cierre VAR/class
    ;;CTRL condiciónr[5]{0} ")"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[4](1) ","
        sub cl, 1     ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto "(" abrir var/class
    ;;CTRL condiciónr[3]{0} "("
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[2](1) "CLASS"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto CLASS
    ;;CTRL condiciónr[1]{0} "CTRL"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;;CTRL condición[0](1) "VAR"
        mov r9, r12     ;obtener el mapa completo
        mov r10, 1      ;constante
        sub cl, 1      ;Añadido 1bit al lector
        shr r9, cl     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz rax, r10    ;compara la zf y lo mueve a rax (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl rax, cl    ;aplica la máscara según el lector
        sub r12, rax    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
        add r15, rax    ;contexto CTRL



;Parser[0]
    ;nif_checker[0]
        ;if["VAR"]
        mov rax, 1      ;Resultado de Éxito
        mov r10, 0	    ;Registro de Fallo
        ;Check 'V'
        mov r9, INPUT[i]	;Cargar 'V'
        xor r9, "V"     	;Si coincide, r9 = 0
        cmovnz r9, r10  	;Si no coincide (no zero), rax = (FALLA)
        ;Check 'A'
        mov r9, INPUT[i+1]  ;Cargar 'A'
        xor r9, "A"     	;Si coincide, r9 = 0
        cmovnz rax, r10  	;Si no coincide (no zero), rax = (FALLA)
        ,Check 'R'
        mov r9, INPUT[i+2]  ;Cargar 'R'
        xor r9, "R"     	;Si coincide, r9 = 0
        cmovnz rax, r10  	; Si falla (r9 != 0), rax = 0.
            ;do
            add r12, rax ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        mov rax, 2      ;Resultado de Éxito
        mov r10, 0	    ;Registro de Fallo
        ;Check 'C'
        mov r9, INPUT[i] 	; Cargar 'C'
        xor r9, "C"		 	; Detectar byte
        cmovnz rax, r10  	; Si falla (r9 != 0), rax = 0.
        ;Check 'T'
        mov r9, INPUT[i+1]	; Cargar 'T'
        xor r9, "T"			; Detectar byte
        cmovnz rax, r10		; Comparar byte
        ; Check 'R'
        mov r9, INPUT[i+2]	; Cargar 'R'
        xor r9, "R"			; Detectar byte
        cmovnz rax, r10		; Comparar byte
        ; Check 'L'
        mov r9, INPUT[i+3]	; Cargar 'L'
        xor r9, "L"			; Detectar byte
        cmovnz rax, r10		; Comparar byte
            ;do
            add r8, rax ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        mov rax, 4      ;Resultado de éxito
        mov r10, 0      ;Registro de Fallo
        ; Check C
        mov r9, INPUT[i]
        xor r9, "C"
        cmovnz rax, r10
        ; Check L 
        mov r9, INPUT[i+1]
        xor r9, "L"
        cmovnz rax, r10
        ; Check A 
        mov r9, INPUT[i+2]
        xor r9, "A"
        cmovnz rax, r10
        ; Check S 
        mov r9, INPUT[i+3]
        xor r9, "S"
        cmovnz rax, r10
        ; Check S
        mov r9, INPUT[i+4]
        xor r9, "S"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        mov rax, 0 x40  ;Para guardar
        mov r9, INPUT   ;Para comparar
        xor r9, "("     ;Dirección
        cmovnz rax, r10 ;Operador
            ;do
            add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        mov rax, 0x100
        mov r9, INPUT
        xor r9, ","
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        mov rax 0x400
        mov r9, INPUT
        xor r9, ")"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        mov rax, 0x1000 
		mov r9, INPUT
		xor r9, "{"
		cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        mov rax, 0x4000 
        mov r9, INPUT
        xor r9, "}"
        cmovnz rax, r10

        ;do
            add r8, rax ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        mov rax, 0x10000 
        mov r9, INPUT
        xor r9, "+"
        cmovnz rax, r10
        ;do
            add r8, rax ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        mov rax, 0x40000 
        mov r9, INPUT
        xor r9, "-"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        mov rax, 0x100000 
        mov r9, INPUT
        xor r9, "*"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        mov rax, 0x400000 
        mov r9, INPUT
        xor r9, "/"
        cmovnz rax, r10

            ;do
            add r8, rax ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        mov rax, 0x1000000
        mov r10, 0
        ; Check *
        mov r9, INPUT
        xor r9, "*"
        cmovnz rax, r10
        ; Check *
        mov r9, INPUT[i+1]
        xor r9, "*"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        mov rax, 0x4000000 
        mov r9, INPUT
        xor r9, ";"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
        ;if("=")
        mov rax, 0x10000000 
        mov r9, INPUT
        xor r9, "="
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        mov rax, 0x40000000 
        mov r9, INPUT
        xor r9, '"'
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
        ;if("[")
        mov rax, 0x100000000 
        mov r9, INPUT
        xor r9, "["
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
        ;if("]")
        mov rax, 0x400000000 
        mov r9, INPUT
        xor r9, "]"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
        ;if('.')
        mov rax, 0x1000000000 
        mov r9, INPUT
        xor r9, "."
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
        ;if('nlang')
            mov rax, 0x4000000000 
            mov r10, 0
            ; Check n
            mov r9, INPUT
            xor r9, "n"
            cmovnz rax, r10
            ; Check l
            mov r9, INPUT[i+1]
            xor r9, "l"
            cmovnz rax, r10
            ; Check a
            mov r9, INPUT[i+2]
            xor r9, "a"
            cmovnz rax, r10
            ; Check n
            mov r9, INPUT[1+3]
            xor r9, "n"
            cmovnz rax, r10
            ; Check g
            mov r9, INPUT[1+4]
            xor r9, "g"
            cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[19]) += 1}
        ;if("'")
            mov rax, 0x10000000000 
        	mov r9, INPUT
        	xor r9, "'"
        	cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
        ;if("#")
            mov rax, 0x40000000000 
        	mov r9, INPUT
        	xor r9, "#"
        	cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
        ;if(':')
        mov rax, 0x100000000000 
        mov r9, INPUT
        xor r9, ":"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
        ;if('!')
        mov rax, 0x400000000000 
        mov r9, INPUT
        xor r9, "!"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
        ;if("<")
        mov rax, 0x1000000000000 
        mov r9, INPUT
        xor r9, "<"
        cmovnz rax, r10
            ;do
            add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(">")
        mov rax, 0x1000000000000 
        mov r9, INPUT
        xor r9, ">"
        cmovnz rax, r10
                ;do
                add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(" ")
        mov rax, 0x4000000000000 
        mov r9, INPUT
        xor r9, " "
        cmovnz rax, r10
                ;do
                add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
			
		;if("e")
        mov rax, 0x10000000000000 
        mov r9, INPUT
        xor r9, "e"
        cmovnz rax, r10
                ;do
                add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}

;);
;Parser/Compiler/lexer
;Contexto VAR completo (falta mensaje)
    mov r9, 0 ;comienzo
    ;if["VAR"]
        mov rdx, r15 ;acceder al contexto
        shl rdx, 0   ;dónde estaría el bit de VAR detectado
        and rdx, 1   ;filtro and, para tomar el bit de VAR
        add r9, rdx   ;punto de conexión VAR -> ( -> , -> )
        ;if(" ")
            mov rdx, r15    ;acceder al contexto
            shr rdx, 52     ;ubicación del bit " "
            and rdx, 1      ;filtro and, para tomar el bit de " "
            and r9, rdx      ;Comparación agregado a r9 y conexión
            ;if["("]
                mov rdx, r15    ;acceder al contexto
                shr rdx, 4      ;ubicación bit de "("
                and rdx, 1      ;filtro and
                and r9, rdx     ;lectura agregado a r9
                ;if("umbral")
                    mov rdx, r8         ;Registro de lectura
                    mov rax, 1          ;inicio umbral
                    mov rdx, 1          ;También inicio umbral
                    mov cl, 4           ;desplazador hexadecimal
                    shl rdx, cl          ;x16
                    and rdx, 0xF        ;Límite de 4 bits para el input
                    add rbx, rdx        ;Guardar dígito de umbral en RBX
                    shl rax, cl          ;se agrega el bit del umbral
                ;if[","]
                    mov rdx, 0      ;Reiniciar registro de lectura
                    mov rdx, r15    ;acceder al contexto
                    shr rdx, 8      ;ubicación bit de ","
                    and rdx, 1      ;filtro and 
                    and r9, rdx     ;lectura agregado a r9
                    xor rbx, r9     ;invierte los bits si hay una coma detectada
                    dec rbx         ;para complemento a 2
                        ;if[")"]
                            mov rdx, r15    ;acceder al contexto
                            shr rdx, 10     ;ubicación bit ")"
                            and rdx, 1      ;filtro and
                            and r9, rdx     ;lectura agregado a r9
                              ;if[","]
                                mov rdx, r15    ;acceder al contexto
                                shr rdx, 8      ;ubicación bit de ","
                                and rdx, 1      ;filtro and
                                and r9, rdx     ;lectura agregado a r9 
        ;else("a-z,A-Z,0-9")
            mov rdx, r15        ;Acceder al contexto
            shl rdx, 52         ;Ubicación " "
            and rdx, 1          ;Filtro and
            xor r9, rdx         ;conexión inversa
            xor r9, 1           ;negación
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
        mov rdx, r15        ;acceder al contexto
        shl rdx, 2          ;ubicación CTRL
        and rdx, 1          ;filtro and
        add r9, rdx         ;punto conexión CTRL -> {
        ;if(" ")
            mov rdx, r15    ;acceder al contexto
            shl rdx, 52     ;ubicación del bit " "
            and rdx, 1      ;filtro and, para tomar el bit de " "
            and r9, rdx      ;Comparación agregado a r9 y conexión
            ;if["{"]
                mov rdx, r15    ;acceder al contexto
                shl rdx, 12     ;ubicación del bit "}"
                and rdx, 1      ;filtro and
                and r9, rdx     ;punto conexión { -> ,
                ;if["1/0"]
                    mov rdx, INPUT    ;acceder al dato
                    and rdx, 0x1      ;permite sólo valores binarios
                    and r9, rdx       ;conexión
                    ;if[","]
                        mov rdx, r15    ;acceder al contexto
                        shl rdx, 8      ;ubicación bit de ","
                        and rdx, 1      ;filtro and
                        and r9, rdx     ;punto conexión , -> }
                            ;if["Destino"]
                            mov rdx, INPUT  ;Acceder al input actual
                            xor rax, rdx    ;Xorid 
                                ;if[" "]
                                mov rdx, r15    ;Acceder al contexto
                                shl rdx, 52     ;ubicación del bit " "
                                and rdx, 1      ;Filtro and
                                and r9, rdx     ;Punto de conexión
                                cmovnz rax, ID_DIRECTION
                                    ;if["+"]
                                    mov rdx, r15    ;Acceder al contexto
                                    shl, rdx, 16    ;Ubicación del bit "+"
                                    and rdx, 1      ;Filtro and
                                    and r9, rdx     ;Punto de conexión
                                    ;do
                                    ;si + es correcto 
                                    ;else[!"+"]
                                    mov rdx, r15    ;Acceder al contexto
                                    shl rdx, 16     ;Ubicación del bit +
                                    and rdx, 1      ;Filtro and
                                    xor r9, rdx     ;Punto de conexión
                                    ;do
                                        ;if["-"]
                                        mov rdx, r15 ;Acceder al contexto
                                        shl rdx, 18  ;Ubicación del bit -
                                        and rdx, 1   ;Filtro AND
                                        ;else[!"-"]
                                        mov rdx, r15 ;Acceder al contexto
                                        shl rdx, 18  ;Ubicación del bit -
                                        and rdx, 1   ;Filtro AND
                                        xor r9, rdx  ;Punto de conexión
                                            ;if["*"]
                                            mov rdx, r15 ;Acceder al contexto
                                            shl rdx, 20  ;Ubicación del bit "*"
                                            and rdx, 1   ;Filtro AND
                                            and r9, rdx  ;Punto de conexión
                                            ;do
                                            ;else[!"*"]
                                            mov rdx, r15 ;Acceder al contexto
                                            shl rdx, 20  ;Ubicación del bit "*"
                                            and rdx, 1   ;Filtro AND
                                            xor r9, rdx  ;Punto de conexión
                                            ;do
                                                ;if["**"]
                                                mov rdx, r15 ;Acceder al contexto
                                                shl rdx, 24  ;Ubicación del bit **
                                                and rdx, 1   ;Filtro AND
                                                and r9, rdx  ;Punto de conexión
                                                ;do                                    
                                                ;else[!"**"]
                                                mov rdx, r15 ;Acceder al contexto
                                                shl rdx, 24  ;Ubicación del bit **
                                                and rdx, 1   ;Filtro AND
                                                xor r9, rdx  ;Punto de conexión
                                                ;do
                                                    ;if["/"]
                                                    mov rdx, r15 ;Acceder al contexto
                                                    shl rdx, 22  ;Ubicación del bit /
                                                    and rdx, 1   ;Filtro AND
                                                    and r9, rdx  ;Punto de conexión
                                                    ;do
                                                    ;else[!"/"]
                                                    mov rdx, r15 ;Acceder al contexto
                                                    shl rdx, 22  ;Ubicación del bit /
                                                    and rdx, 1   ;Filtro AND
                                                    xor r9, rdx  ;Punto de conexión
                                                    ;do  
                            ;if["}"]
                                mov rdx, r15    ;acceder al conexto
                                shl rdx, 14     ;ubicación del bit "}"
                                and rdx, 1      ;filtro and
                                and r9, rdx     ;conexión
                                ;if[","]
                                    mov rdx, r15    ;acceder al contexto
                                    mov cl, 8       ;dirección ","
                                    shl rdx, cl      ;ubicación bit de ","
                                    and rdx, 1      ;filtro and
                                    and r9, rdx      ;lectura agregado a r9
        ;else("a-z,A-Z,0-9")
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
        mov rdx, r15        ;acceder al contexto
        shl rdx, 4          ;ubicación CLASS
        and rdx, 1          ;filtro and
        mov r9, rdx         ;punto conexión CLASS -> =
        ;if[" "]
            mov rdx, r15        ;Acceder al contexto
            shl rdx, 52         ;Ubicación " "
            and rdx, 1          ;Filtro and
            and r9, rdx         ;conexión
            ;if["="]
                mov rdx, r15    ;acceder al contexto
                shl rdx, 28     ;ubicación =
                and rdx, 1      ;filtro and
                and r9, rdx     ;punto conexión = -> (
                ;if[("("]
                    mov rdx, r15    ;acceder al contexto
                    shl rdx, 12     ;ubicación (
                    and rdx, 1      ;filtro and
                    and r9, rdx     ;punto conexión ( -> VAR o CTRL
                    ;if["VAR"]
                        mov rdx, r15    ;acceder al contexto
                        shl rdx, 0    ;ubicación VAR
                        and rdx, 1      ;filtro and
                        and r9, rdx      ;punto conexión ( -> VAR
                            ;end
                                mov r9, 0       ;Reiniciar contexto
                    ;else["CTRL"]
                    mov rdx, r15    ;acceder al contexto
                    shl rdx, 2      ;Ubicación de CTRL
                    and rdx, 1      ;filtro and 
                    mov r9, rdx     ;punto conexión ( -> CTRL
                        ;end
                        mov r9, 0     ;Reiniciar contexto
    ;if[!" "]
        mov rdx, r15        ;Acceder al contexto
        shl rdx, 52         ;Ubicación " "
        and rdx, 1          ;Filtro and
        xor r9, rdx         ;conexión
        mov rax, rdx        ;Iniciamos el acumulador
        shl rax, 9          ;1 byte + 1 bit
        sub rax, 1          ;restar 1 para que sea FF
        and rax, INPUT      ;ingresamos el byte
        xor rax, r13        ;xor index
        add r13, rax        ;añadir resultado de la xor
        shl r13, rcx        ;desplazar según contador
        add rcx, 1          ;aumentar contador en 1
    ;else[")"]
    mov rdx, r15        ;acceder al contexto
    shl rdx, 10         ;ubicación )
    and rdx, 1          ;filtro and
    mov r9, rdx         ;punto conexión ) -> ;
        ;end
        mov r9, 0       ;Reiniciar contexto
        ;if(";")
        mov rdx, r15        ;acceder al contexto
        shl rdx, 26         ;ubicación ;
        and rdx, 1          ;and
        mov r9, rdx         ;lectura agreado a r9
    ;end
