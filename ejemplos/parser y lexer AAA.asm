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

_start
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

    ;Otra clase
    ;1 "["                 ;keyword load and save (start)
    ;2 "]"                 ;keyword load and save (end)
    ;3 "."                 ;keyword extension save/load
    ;4 "N"                 ;keyword extension N-Lang
    ;5 "'"                 ;Subkeyword string2
    ;#" no hace falta, ya que la condición: hacer nada y/o ignorar es gratuita
    ;Error, el # no es simplemente "hacer nada" es "ignorar hasta recibir un salto de línea" 
    ;6 "#"                 ;Coemntarios
    ;7 ";"                 ;Otra Subekeyword de asignación y/o división
    ;8 "!"                 ;subkeyword para not
;nif[0](16) = CLASS nif = (
    mov rdx, 0      ;contador de bits
    mov r8, 0       ;clase principal nif(1)
    ;VAR condición[0](1) "VAR"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[0]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS (01)
    ;VAR condición[1](1) "CTRL"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[1]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[2](1) "CLASS"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[2]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
    ;VAR condición[3](1) "("
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[3]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[4](1) ","
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[4]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[5](1) ")"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[5]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[6](1) "{"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[6]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[7](1) "}"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[7]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[8](1) "+"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[8]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[9](1) "-"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[9]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[10](1) "*"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[10]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[11](1) "/"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[11]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[12](1) "**"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[12]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[13](1) ";"
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[13]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[14](1) "="
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[14]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS
    ;VAR condición[15](1) '"'
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 3       ;añadido VAR(1) (11)
        add r8, r9      ;añadido a la CLASS
    ;CTRL separador[15]{0} 
        mov r9, 1       ;registro de operación
        add rdx, 2      ;añadido 2bits al lector
        shl r9, rdx     ;desplazar r9 lo que nos marca el lector
        add r9, 1       ;añadido CTRL{0} (01)
        add r8, r9      ;añadido a la CLASS    
;);
;Actualizar y comparar, mediante cmp zf
    mov rdx, r12    ;Registro lectura
    
    ;CTRL separador[15]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0 (si se activó)
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[15](1) '"'
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto '"' (para strings)
    ;CTRL separador[14]{0}
        mov r9, r8     ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[14](1) "="
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "=" para asignación
    ;CTRL separador[13]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[13](1) ";"
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto ";" borra contexto de otras keywords y subkeywords
    ;CTRL separador[12]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[12](1) "**"
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "**" para detectar exponente
    ;CTRL separador[11]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[11](1) "/"
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "/" para detectar divisor
    ;CTRL separador[10]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[10](1) "*"
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "*" para detectar factor
    ;CTRL separador[9]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[9](1) "-"
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "-" para detectar substraendo
    ;CTRL separador[8]{0}
        mov r9, r8      ;obtener el mapa completo      
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[8](1) "+"
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "+" para detectar sumando
    ;CTRL separador[7]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[7](1) "}"
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "}" cierre de CTRL
    ;CTRL separador[6]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[6](1) "{"
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "{" abrir CTRL
    ;CTRL separador[5]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[5](1) ")"
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto ")" cierre VAR/class
    ;CTRL separador[4]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[3](1) "("
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto "(" abrir var/class
    ;CTRL separador[2]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[2](1) "CLASS"
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto CLASS
    ;CTRL separador[1]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[1](1) "CTRL"
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto CTRL
    ;CTRL separador[0]{0}
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r8, r11     ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[0](1) "VAR"
        mov r9, r8      ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r8, r11     ;reinicia el bit si resultó cambiado
        add r10, r11    ;contexto VAR

;Otra clase
    ;nif[1](6) = CLASS nif = (
        mov rdx, 0      ;contador de bits
        mov r13, 0       ;clase principal nif(1)
        ;VAR condición[0](1) "["
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[0]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[1](1) "]"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[1]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[2](1) "."
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[2]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[3](1) "N"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[3]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[4](1) "'"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[4]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[5](1) "#"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[5]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[6](1) ":"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[6]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
        ;VAR condición[6](1) "!"
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 3       ;añadido VAR(1) (11)
            add r13, r9     ;añadido a la CLASS
        ;CTRL separador[6]{0} 
            mov r9, 1       ;registro de operación
            add rdx, 2      ;añadido 2bits al lector
            shl r9, rdx     ;desplazar r9 lo que nos marca el lector
            add r9, 1       ;añadido CTRL{0} (01)
            add r13, r9     ;añadido a la CLASS
    ;);
;Actualizar y comparar, mediante cmp zf
    mov rdx, r12    ;Registro lectura
    ;CTRL separador[6]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[6](1) "!"
        sub rdx, 1      ;Añadido 1bit al lector
        mov r9, r13     ;Obtener el mapa completo
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto "!" not
    ;CTRL separador[6]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[6](1) ":"
        sub rdx, 1      ;Añadido 1bit al lector
        mov r9, r13     ;Obtener el mapa completo
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto ":" división/aignación
    ;CTRL separador[5]{0}
        mov r9, r13     ;Obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[5](1) "#"
        sub rdx, 1      ;Añadido 1bit al lector
        mov r9, r13     ;Obtener el mapa completo
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto "#" comentarios
    ;CTRL separador[4]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[3](1) "'"
        sub rdx, 1      ;Añadido 1bit al lector
        mov r9, r13     ;Obtener el mapa completo
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto "'" string2
    ;CTRL separador[2]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[2](1) "N"
        mov r9, r12     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto N extensión de archivo
    ;CTRL separador[1]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[1](1) "]" 
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto ] cerrar load/save
    ;CTRL separador[0]{0}
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 1    ;compara la zf y lo mueve a r11
        shl r11, rdx    ;aplica la máscara según el lector
        sub r13, r11    ;reinicia el bit si resultó cambiado (los ctrl si están activos, son 10, el sub, los vuelve a 01)
    ;VAR condición[0](1) "["
        mov r9, r13     ;obtener el mapa completo
        sub rdx, 1      ;Añadido 1bit al lector
        shr r9, rdx     ;desplazado r9 lo que nos marca el lector
        and r9, 0x1     ;toma un solo bit
        cmp r9, 0       ;compara si el slot es 0
        cmovz r11, 3    ;compara la zf y lo mueve a r11 (para las VAR se requiere 3 (11), para pasar de 0 a 33)
        shl r11, rdx    ;aplica la máscara según el lector
        add r13, r11    ;reinicia el bit si resultó cambiado
        add r14, r11    ;contexto [ abrir load/save

;Parser[1]
    ;nif[1]
        ;if["["]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "["     ;Detectar [
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "["     ;Si r9 = 0 -> 0, si r9 = 255 -> "["
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;[ detect
        cmovz r15, 1
            ;do
            add r8, r15 ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["]"]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "]"     ;Detectar ]
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "]"     ;Si r9 = 0 -> 0, si r9 = 255 -> "]"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;] detect
        cmovz r15, 0x10
            ;do
            add r8, r15 ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["."]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "."     ;Detectar (
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "."     ;Si r9 = 0 -> 0, si r9 = 255 -> "."
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;. detect
        cmovz r15, 0x100
            ;do
            add r8, r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("N")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "N"     ;Detectar N
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "N"     ;Si r9 = 0 -> 0, si r9 = 255 -> "N"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;N detect
        cmovz r15, 0x1000
            ;do
            add r8, r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if("'")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "'"     ;Detectar ''
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "'"     ;Si r9 = 0 -> 0, si r9 = 255 -> "'"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;' detect
        cmovz r15, 0x10000
            ;do
            add r8, r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if("#")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "#"     ;Detectar #
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "#"     ;Si r9 = 0 -> 0, si r9 = 255 -> "#"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;# detect
        cmovz r15, 0x100000
            ;do
            add r8, r11 ;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if(":")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, ":"     ;Detectar :
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ":"     ;Si r9 = 0 -> 0, si r9 = 255 -> ":"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;: detect
        cmovz r15, 0x1000000
            ;do
            add r8, r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("!")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "!"     ;Detectar :
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "!"     ;Si r9 = 0 -> 0, si r9 = 255 -> ":"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;: detect
        cmovz r15, 0x1000000
            ;do
            add r8, r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
;);
;Parser[0]
    ;nif[0]
        ;if["VAR"]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "V"     ;Detectar V
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "V"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "A"     ;Detectar A
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "A"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, 0       ;Operador
        cmp r9, "R"     ;Detectar R
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "R"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;VAR detect
        cmovz r15, 1
            ;do
            add r8, r15 ;CTRL[0] {1, nif[0]((VAR[0]) += 1}
        ;if["CTRL"]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "C"     ;Detectar C
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "C"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "T"     ;Detectar T
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "T"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "R"     ;Detectar R
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "R"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "L"     ;Detectar L
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "L"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;CTRL detect
        cmovz r15, 0x10 
            ;do
            add r8, r15 ;CTRL[1] {1, nif[0]((VAR[1]) += 1}
        ;if["CLASS"]
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "C"     ;Detectar C
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "C"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "L"     ;Detectar L
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "L"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "A"     ;Detectar A
        shl r9, 8       ;Dejar un espacio de un byte
        cmovz r9, 255   ;añadir filtro and
        and r9, "A"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "S"     ;Detectar S
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "S"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        mov r9, INPUT   ;Operador
        cmp r9, "S"     ;Detectar S
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Dejar un espacio de un byte
        and r9, "S"     ;Añadir el byte
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;CLASS detect
        cmovz r15, 0x100
            ;do
            add r8, r15 ;CTRL[2] {1, nif[0]((VAR[2]) += 1}
        ;if("(")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "("     ;Detectar (
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "("     ;Si r9 = 0 -> 0, si r9 = 255 -> "("
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz r15, 0x1000
            ;do
            add r8, r15 ;CTRL[3] {1, nif[0]((VAR[3]) += 1}
        ;if(",")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, ","     ;Detectar ,
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ","     ;Si r9 = 0 -> 0, si r9 = 255 -> ","
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;, detect
        cmovz r15, 0x10000
            ;do
            add r8, r15 ;CTRL[4] {1, nif[0]((VAR[4]) += 1}
        ;if(")")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, ")"     ;Detectar )
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ")"     ;Si r9 = 0 -> 0, si r9 = 255 -> ")"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;) detect
        cmovz r15, 0x100000
            ;do
            add r8, r15 ;CTRL[5] {1, nif[0]((VAR[5]) += 1}
        ;if("{")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "{"     ;Detectar {
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "{"     ;Si r9 = 0 -> 0, si r9 = 255 -> "{"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;{ detect
        cmovz r15, 0x1000000
            ;do
            add r8, r15 ;CTRL[6] {1, nif[0]((VAR[6]) += 1}
        ;if("}")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "}"     ;Detectar }
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "}"     ;Si r9 = 0 -> 0, si r9 = 255 -> "}"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;} detect
        cmovz r15, 0x10000000
            ;do
            add r8, r15 ;CTRL[7] {1, nif[0]((VAR[7]) += 1}
        ;if("+")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "+"     ;Detectar +
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "+"     ;Si r9 = 0 -> 0, si r9 = 255 -> "+"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;+ detect
        cmovz r15, 0x100000000
            ;do
            add r8, r15 ;CTRL[8] {1, nif[0]((VAR[8]) += 1}
        ;if("-")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "-"     ;Detectar -
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "-"     ;Si r9 = 0 -> 0, si r9 = 255 -> "-"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;- detect
        cmovz r15, 0x1000000000
            ;do
            add r8, r15 ;CTRL[9] {1, nif[0]((VAR[9]) += 1}
        ;if("*")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar *
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;* detect
        cmovz r15, 0x10000000000
            ;do
            add r8, r15 ;CTRL[10] {1, nif[0]((VAR[10]) += 1}
        ;if("/")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "/"     ;Detectar /
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "/"     ;Si r9 = 0 -> 0, si r9 = 255 -> "/"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;/ detect
        cmovz r15, 0x100000000000
            ;do
            add r8, r15 ;CTRL[11] {1, nif[0]((VAR[11]) += 1}
        ;if("**")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar *
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;* detect
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, "*"     ;Detectar (
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, "*"     ;Si r9 = 0 -> 0, si r9 = 255 -> "*"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;** detect
        cmovz r15, 
        cmovz r15, 0x1000000000000
            ;do
            add r8, r15 ;CTRL[12] {1, nif[0]((VAR[12]) += 1}
        ;if(";")
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, ";"     ;Detectar ;
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, ";"     ;Si r9 = 0 -> 0, si r9 = 255 -> ";"
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;; detect
        cmovz r15, 0x100000000000000
            ;do
            add r8, r15 ;CTRL[14] {1, nif[0]((VAR[14]) += 1}
        ;if('"')
        mov rdx, 0      ;Para guardar
        mov r15, 0      ;Para comparar
        mov r9, INPUT   ;Operador
        cmp r9, '"'     ;Detectar "
        cmovz r9, 255   ;añadir filtro and
        shl r9, 8       ;Añadir el byte
        and r9, '"'     ;Si r9 = 0 -> 0, si r9 = 255 -> '"'
        or rdx, r9      ;colocar el byte
        cmp rdx, INPUT  ;( detect
        cmovz r15, 0x1000000000000000
            ;do
            add r8, r15 ;CTRL[15] {1, nif[0]((VAR[15]) += 1}
;);
;Parser/Compiler/lexer
    ;if["VAR"]
    
    mov rdx, r10 ;acceder al contexto
    shl rdx, 0   ;dónde estaría el bit de VAR detectado
    and rdx, 3   ;filtro and, para tomar el bit de VAR
    add r9, rdx  ;punto de conexión VAR -> ( -> , -> )
    ;Contexto VAR    
        ;if["("]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x1000 ;ubicación bit de "("
        and rdx, 3      ;filtro and
        xor r15, r9     ;filtro xor encadenamiento condicional 
        add r9, rdx     ;lectura agregado a r9
        add r9, r15     ;punto conexión ( -> , -> )
        ;if[","]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x10000 ;ubicación bit de "("
        and rdx, 3      ;filtro and
        xor r15, r9     ;filtro xor encadenamiento condicional 
        add r9, rdx     ;lectura agregado a r9
        add r9, r15     ;punto conexión ( -> , -> )

        ;if[")"]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x100000 ;ubicación bit ")"
        and rdx, 3      ;filtro and
        xor r15, r9     ;filtro xor encadenamiento condicional
        add r9, rdx     ;lectura agregado a r9
        add r9, r15     ;punto conexión )
        
        ;if[","]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x10000 ;ubicación bit de "("
        and rdx, 3      ;filtro and
        xor r15, r9     ;filtro xor encadenamiento condicional 
    ;end
    ;if["CTRL"]
    mov r9, 0           ;reinicio contexto
    mov rdx, r10        ;acceder al contexto
    shl rdx, 0x10       ;ubicación CTRL
    and rdx, 3          ;filtro and
    add r9, rdx         ;punto conexión CTRL -> {
        ;if["{"]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x1000000 ;ubicación del bit "}"
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor encadenamiento condiconal
        add r9, r15     ;punto conexión { -> ,
        ;if[","]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x10000 ;ubicación bit de ","
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor encadenamiento condicional 
        add r9, r15     ;punto conexión , -> } 
        ;if["}"]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al conexto
        shl rdx, 0x10000000 ;ubicación del bit "}"
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor, encadenamiento condiconal
        add r9, r15     ;punto conexión } ->
        ;if[","]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x10000 ;ubicación bit de "("
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor encadenamiento condicional
    ;end
    ;if["CLASS"]
    mov r9, 0           ;reinicio contexto
    mov rdx, r10        ;acceder al contexto
    shl rdx, 0x100      ;ubicación CLASS
    and rdx, 3          ;filtro and
    add r9, rdx     ;lectura agregado a r9
    xor r15, r9         ;filtro xor, encadenamiento condicional
    add r9, r15         ;punto conexión CLASS -> =
        ;if["="]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x100000000000000 ;ubicación =
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor, encadenamiento condicional
        add r9, r15     ;punto conexión = -> (
        ;if[("("]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x1000 ;ubicación (
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor, encadenamiento condicional
        add r9, r15     ;punto conexión ( -> VAR o CTRL
        ;if["VAR"]
        mov r15, 0      ;registro de cadena
        mov rdx, r10    ;acceder al contexto
        shl rdx, 0x1    ;ubicación VAR
        and rdx, 3      ;filtro and
        add r9, rdx     ;lectura agregado a r9
        xor r15, r9     ;filtro xor, encadenamiento condicional
        add r9, r15     ;punto conexión ( -> VAR
        ;end
        ;else["CTRL"]
        mov r15, 0  ;registro cadena
        mov rdx, r10;acceder al contexto
        and rdx, 3  ;filtro and
        add r9, rdx ;lectura agregado a r9
        not r9, r9  ;negar la condición
        xor r15, r9 ;filtro xor, encadenamiento condicional
        add r9, r15 ;punto conexión ( -> CTRL
        ;end
    ;else[")"]
    mov r15, 0       ;reinicio contexto
    mov rdx, r10    ;acceder al contexto
    shl rdx, 0x100000;ubicación )
    and rdx, 3      ;filtro and
    add r9, rdx     ;lectura agregado a r9
    xor r15, r9     ;filtro xor
    not r9, r9      ;motor else
    add r9, r15     ;punto conexión ) -> ;
        ;if(";")
        mov r15, 0  ;registro cadena
        mov rdx, r10;acceder al contexto
        shl rdx, 0x10000000000000 ;ubicación ;
        and rdx, 3  ;and
        add r9, rdx ;lectura agreado a r9
        xor r15, r9 ;filtro xor
    ;end