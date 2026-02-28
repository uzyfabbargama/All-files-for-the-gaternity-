;Template listo para agregar la unión de registros
    ;mov r8,1   ;registro de operaciones
    ;shl r8, 63 ;activar último bit
    ;mov r9, r8 ;guardar último bit
    ;mov r8, 0  ;vaciar
    ;uso
    ;mov r8, INPUT ;valor de entrada
    ;xor r10, r8   ;1 (false), 0 (true)
    ;not r11, r10  ;guardamos el valor inverso
    ;sh r11, 63    ;tomamos el acarreeo
    ;add r12, r11  ;conexión final r8 se conectó correctamente con r12
    ;Fin de template

;lista de registros fantasma inexistentes
    ;rfx no existe es r9
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
    ;r12 PG #CLASS keywords 1-24
    ;r13 PG para ID
    ;r14 PG libre
    ;r15 PG #contexto keywords 1-24
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
    ;CTRL condición[24](1) "<"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (11)
        add r12, r9     ;añadido a la CLASS
    ;CTRL condición[25](1) ">"
        mov r9, 1       ;registro de operación
        add cl, 2      ;añadido 2bits al lector
        shl r9, cl     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido VAR(1) (11)
        add r12, r9     ;añadido a la CLASS
;);
;Actualizar y comparar, mediante cmp zf
    ;CL = cantidad de bits
    
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
    ;;CTRL condición[24](1) "<"
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
    ;nif[0]
        ;if["VAR"]
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Constante
        mov r10, 1      ;Direección
        mov r9, INPUT   ;Operador
        cmp r9, "V"     ;Detectar V
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "V"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "A"     ;Detectar A
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "A"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, 0       ;Operador
        cmp r9, "R"     ;Detectar R
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "R"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;VAR detect
        cmovz rax, r10
            ;do
            add r12, rax ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        mov rdx, 0      ;Para guardar
        mov rax, 55     ;Para comparar
        mov r10, 4      ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "C"     ;Detectar C
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "C"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "T"     ;Detectar T
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "T"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "R"     ;Detectar R
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "R"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "L"     ;Detectar L
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "L"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;CTRL detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x10   ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "C"     ;Detectar C
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "C"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "L"     ;Detectar L
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "L"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "A"     ;Detectar A
        shl r9, 8       ;Dejar un espacio de un byte
        cmovz r9, rax   ;añadir filtro and
        and r9, "A"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "S"     ;Detectar S
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "S"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "S"     ;Detectar S
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "S"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;CLASS detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x40   ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "("     ;Detectar (
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "("     ;Si r9 = 0 -> 0, si r9 = 255 -> "("
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x100  ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, ","     ;Detectar ,
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ","     ;Si r9 = 0 -> 0, si r9 = 255 -> ","
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;, detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x400  ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, ")"     ;Detectar )
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ")"     ;Si r9 = 0 -> 0, si r9 = 255 -> ")"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;) detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x1000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "{"     ;Detectar {
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "{"     ;Si r9 = 0 -> 0, si r9 = 255 -> "{"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;{ detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x4000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "}"     ;Detectar }
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "}"     ;Si r9 = 0 -> 0, si r9 = 255 -> "}"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;} detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x10000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "+"     ;Detectar +
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "+"     ;Si r9 = 0 -> 0, si r9 = 255 -> "+"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;+ detect
        cmovz rax, rax
            ;do
            add r8, rax ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x40000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "-"     ;Detectar -
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "-"     ;Si r9 = 0 -> 0, si r9 = 255 -> "-"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;- detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x100000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar *
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;* detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x400000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "/"     ;Detectar /
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "/"     ;Si r9 = 0 -> 0, si r9 = 255 -> "/"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;/ detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x1000000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar *
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;* detect
        mov rdx, 0      ;Para guardar
        mov rax, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar (
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;** detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x4000000;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, ";"     ;Detectar ;
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ";"     ;Si r9 = 0 -> 0, si r9 = 255 -> ";"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;; detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[14] {1, nif[0]((VAR[13]) += 1}
        ;if("=")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x10000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, ";"     ;Detectar ;
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ";"     ;Si r9 = 0 -> 0, si r9 = 255 -> ";"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;; detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x4000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
        ;if("[")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x100000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[16]) += 1}
        ;if("]")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x400000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[17]) += 1}
        ;if('.')
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x1000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[18]) += 1}
        ;if('nlang')
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x4000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, 'n'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, 'n'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        mov rax, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, 'l'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, 'l'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        mov rax, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, 'a'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, 'a'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        mov rax, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, 'n'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, 'n'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        mov rax, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, 'g'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, 'g'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[19]) += 1}
        ;if("'")
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x10000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[20]) += 1}
        ;if("#")
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x40000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[21]) += 1}
        ;if(':')
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x100000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[22]) += 1}
        ;if('!')
        mov rdx, 0      ;Para guardar
        mov rax, 255      ;Para comparar
        mov r10, 0x40000000000 ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[15] {1, nif[0]((VAR[23]) += 1}
        ;if("<")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x10000000000000   ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, "<"     ;Detectar (
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "<"     ;Si r9 = 0 -> 0, si r9 = 255 -> "("
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
            ;if(">")
        mov rdx, 0      ;Para guardar
        mov rax, 255    ;Para comparar
        mov r10, 0x40000000000000   ;Dirección
        mov r9, INPUT   ;Operador
        cmp r9, ">"     ;Detectar (
        cmovz r9, rax   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ">"     ;Si r9 = 0 -> 0, si r9 = 255 -> "("
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz rax, r10
            ;do
            add r8, rax ;CTRL[3] {1, nif[0]((VAR[3]) += 1}

;);
;Parser/Compiler/lexer
;Contexto VAR
    ;if["VAR"]
        mov rdx, r15 ;acceder al contexto
        shl rdx, 0   ;dónde estaría el bit de VAR detectado
        and rdx, 1   ;filtro and, para tomar el bit de VAR
        or r9, rdx   ;punto de conexión VAR -> ( -> , -> )
        ;if(" ")
            mov rdx, 0      ;Registro de lectura
            mov rax, 1      ;iniciamos la cadena
            mov rdx, " "    ;Inicializamos el valor a detectar (espacio)
            cmp rdx, INPUT  ;Detecta un espacio
            cmovz r8, rax     ;Detecta si es true
            and r9, r8      ;Comparación agregado a r9 y conexión
            ;if["("]
                mov rax, 0      ;registro de cadena
                mov rdx, r15    ;acceder al contexto
                shr rdx, 4      ;ubicación bit de "("
                and rdx, 1      ;filtro and
                xor rax, r9     ;filtro xor encadenamiento condicional 
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
                    mov rax, 0      ;registro de cadena
                    shr rdx, 8      ;ubicación bit de ","
                    and rdx, 1      ;filtro and
                    xor rax, r9     ;filtro xor encadenamiento condicional 
                    and r9, rdx     ;lectura agregado a r9
                    xor rbx, r9     ;invierte los bits si hay una coma detectada
                    dec rbx         ;para complemento a 2
                        ;if[")"]
                            mov rax, 0      ;registro de cadena
                            mov rdx, r15    ;acceder al contexto
                            shr rdx, 10     ;ubicación bit ")"
                            and rdx, 1      ;filtro and
                            xor rax, r9     ;filtro xor encadenamiento condicional
                            and r9, rdx     ;lectura agregado a r9
                              ;if[","]
                                mov rax, 0      ;registro de cadena
                                mov rdx, r15    ;acceder al contexto
                                shr rdx, 8      ;ubicación bit de "("
                                and rdx, 1      ;filtro and
                                xor rax, r9     ;filtro xor encadenamiento condicional 
        ;else("a-z,A-Z,0-9")
            mov rax, 1      ;Iniciamos el acumulador
            add rax, INPUT  ;ingresamos el byte
            mov r13, 0      ;Ingresamos la memoria ID
            xor rax, rbx    ;xor index
            add r13, rax    ;añadir resultado de la xor
            shl r13, rcx    ;desplazar según contador
    ;end
        mov r9, 0           ;reinicio contexto
    ;if["CTRL"]
        mov rdx, r15        ;acceder al contexto
        shr rdx, 2          ;ubicación CTRL
        and rdx, 1          ;filtro and
        mov r9, rdx         ;punto conexión CTRL -> {
        ;if(" ")
            ;if["{"]
                mov rax, 0      ;registro de cadena
                mov rdx, r15    ;acceder al contexto
                shr rdx, 12     ;ubicación del bit "}"
                and rdx, 1      ;filtro and
                mov r9, rdx     ;lectura agregado a r9
                xor rax, r9     ;filtro xor encadenamiento condiconal
                or r9, rax      ;punto conexión { -> ,
                ;if[","]
                    mov rax, 0      ;registro de cadena
                    mov rdx, r15    ;acceder al contexto
                    shr rdx, 8      ;ubicación bit de ","
                    and rdx, 1      ;filtro and
                    mov r9, rdx     ;lectura agregado a r9
                    xor rax, r9     ;filtro xor encadenamiento condicional 
                    or r9, rax      ;punto conexión , -> } 
                    ;if["}"]
                        mov rax, 0      ;registro de cadena
                        mov rdx, r15    ;acceder al conexto
                        shr rdx, 14     ;ubicación del bit "}"
                        and rdx, 1      ;filtro and
                        mov r9, rdx     ;lectura agregado a r9
                        xor rax, r9     ;filtro xor, encadenamiento condiconal
                        or r9, rax      ;punto conexión } ->
                    ;if[","]
                            mov rax, 0      ;registro de cadena
                            mov rdx, r15    ;acceder al contexto
                            mov cl, 8       ;dirección ","
                            shr rdx, cl      ;ubicación bit de ","
                            and rdx, 1      ;filtro and
                            or r9, rdx      ;lectura agregado a r9
                            xor rax, r9     ;filtro xor encadenamiento condicional
        ;else(a-z,A-Z,0-9)
    ;end
    ;if["CLASS"]
    mov r9, 0           ;reinicio contexto
    mov rdx, r15        ;acceder al contexto
    shl rdx, 4          ;ubicación CLASS
    and rdx, 1          ;filtro and
    mov r9, rdx         ;lectura agregado a r9
    xor rax, r9         ;filtro xor, encadenamiento condicional
    or r9, rax          ;punto conexión CLASS -> =
        ;if["="]
        mov rax, 0      ;registro de cadena
        mov rdx, r15    ;acceder al contexto
        shl rdx, 28     ;ubicación =
        and rdx, 1      ;filtro and
        mov r9, rdx     ;lectura agregado a r9
        xor rax, r9     ;filtro xor, encadenamiento condicional
        or r9, rax      ;punto conexión = -> (
        ;if[("("]
        mov rax, 0      ;registro de cadena
        mov rdx, r15    ;acceder al contexto
        shl rdx, 12     ;ubicación (
        and rdx, 1      ;filtro and
        or r9, rdx      ;lectura agregado a r9
        xor rax, r9     ;filtro xor, encadenamiento condicional
        add r9, rax     ;punto conexión ( -> VAR o CTRL
        ;if["VAR"]
        mov rax, 0      ;registro de cadena
        mov rdx, r15    ;acceder al contexto
        shl rdx, 0    ;ubicación VAR
        and rdx, 1      ;filtro and
        mov r9, rdx     ;lectura agregado a r9
        xor rax, r9     ;filtro xor, encadenamiento condicional
        or r9, rax      ;punto conexión ( -> VAR
        ;end
        ;else["CTRL"]
        mov rax, 0      ;registro cadena
        mov rdx, r15    ;acceder al contexto
        and rdx, 1      ;filtro and 
        mov r9, rdx     ;lectura agregado a r9
        not r9, r9      ;negar la condición
        xor rax, r9     ;filtro xor, encadenamiento condicional
        or r9, rax      ;punto conexión ( -> CTRL
        ;end
    ;else[")"]
    mov rax, 0          ;reinicio contexto
    mov rdx, r15        ;acceder al contexto
    shl rdx, 10         ;ubicación )
    and rdx, 1          ;filtro and
    mov r9, rdx         ;lectura agregado a r9
    xor rax, r9         ;filtro xor
    not r9, r9          ;motor else
    or r9, rax          ;punto conexión ) -> ;
        ;if(";")
        mov rax, 0          ;registro cadena
        mov rdx, r15        ;acceder al contexto
        shl rdx, 26         ;ubicación ;
        and rdx, 1          ;and
        mov r9, rdx         ;lectura agreado a r9
        xor rax, r9         ;filtro xor
    ;end