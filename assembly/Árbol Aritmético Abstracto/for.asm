_start:
    ;CLASS for(in, to, each) = (VAR in, VAR to, VAR each, CTRL bucle{1, in += (in < to)* each})
        mov r12, in      ;in 
        mov r13, to      ;to
        mov r14, each    ;each
        mov rdx, r12     ;comparar
        cmpl rdx, r13    ;in - to = to mayor
        cmovl r11, 1   ;si data es less
        mul r11, r14
        add r12, r11
        ;¿terminó el bucle?
        and r15, 1
        not r11
;aquí lo unes con otros sistemas


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