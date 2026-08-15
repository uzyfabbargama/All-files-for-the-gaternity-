; ============================================
; MANEJO DE BUCLES (Preprocesado + O(1))
; ============================================
%macro crear_loop 0
    mov al, [font_code+rsi]
    cmp al, "["
    jne %%exit
    
    mov r11, rsi           ; guardamos posición de '['
    add rsi, 1             ; buscamos ']'
%%seek:
    add rsi, 1
    mov rax, [font_code+rsi]
    ror rax, 8
    
    xor r9, r9          ; r9 va a ser nuestro "contador de bytes avanzados"
    mov cl, 1           ; Inicializamos cl en 1 (buscando)
    
    %rep 8
        cmp al, "]"
        setnz r10b      ; r10b = 1 si NO es ']', 0 si SÍ es ']'
        and cl, r10b    ; cl se mantiene en 1 SOLO si todavía no encontramos el ']'
        
        ; Si cl es 1, sumamos 1 a r9. Si cl cayó a 0 (porque encontramos ']'), sumamos 0.
        movzx rdx, cl
        add r9, rdx     
        
        shl r10b, 3     ; 8 o 0
        shr rax, cl     ; Desplazamiento controlado
    %endrep
    
    ; Al salir del %rep 8:
    ; Si cl == 1, significa que en estos 8 bytes NO había ningún ']'.
    ; Si cl == 0, ¡LO ENCONTRAMOS! Y r9 tiene la cantidad exacta de bytes hasta el ']'.
    
    test cl, cl
    jnz %%seguir_buscando
    
    ; --- ¡ENCONTRADO! ---
    add rsi, r9         ; Ahora rsi apunta EXACTAMENTE al ']' correcto.
    mov rdx, rsi        ; rdx tiene la posición real de ']' para acoplar con r11 ([)
    jmp %%exit

%%seguir_buscando:
    add rsi, 7          ; Como no estaba acá, saltamos el bloque completo
    jmp %%seek
    
    ; Guardar en cell[rbx + 1 + posición_de_'[']
    mov r10d, r11d
    shl r10, 3
    add r10, 1
    mov [cell+r10], esi    ; guardar posición de ']'
    
    ; Guardar en cell[rbx + 1 + posición_de_']']
    mov r10d, esi
    shl r10, 3
    add r10, 1
    mov [cell+r10], r11d   ; guardar posición de '['
%%exit:
%endmacro

%macro access_bucle_start 0
    mov al, [font_code+rsi] ;vemos un byte
    cmp al, "[" ;comparamos ese byte
    setz al ;si es verdadero, lo hacemos 1, 0 sino
    and al, 1 ;limpiamos los 8 bits
    shl rax, 8 ;ahora hacemos que lo de al, se vaya a ah
    mov r10, rbx ;sabemos que rbx tiene el puntero a la celda, lo movemos
    mov al, [cell+r10] ;vemos el valor de la celda actual
    cmp al, 0 ;comparamos si es 0
    setz al ; tenemos el bit
    and al, 1 ;lo aislamos
    and al, ah ;al tiene el "si es 0" y ah tiene el "si es '['", y si ambos son correctos, ignoramos el salto y seguimos
    jz %%exit
    mov r10d, esi ;vamos al puntero de la celda
    shr r10, 3 ;la memoria de doble propósitco
    add r10, 1 ;revisamos el lugar de al lado
    mov esi, [cell+r10] ;movemos el puntero de instrucción para hacer el salto
    and rsi, -1 ;teoricamente 32 bits
%%exit: ;salimos
%endmacro

%macro access_bucle_end 0
    mov al, [font_code+rsi] ;vemos un byte
    cmp al, "]" ;comparamos ese byte
    setz al ;si es verdadero, lo hacemos 1, 0 sino
    and al, 1 ;limpiamos los 8 bits
    shl rax, 8 ;ahora hacemos que lo de al, se vaya a ah
    mov r10, rbx ;sabemos que rbx tiene el puntero a la celda, lo movemos
    mov al, [cell+r10] ;vemos el valor de la celda actual
    cmp al, 0 ;comparamos si es 0
    setnz al ; tenemos el bit
    and al, 1 ;lo aislamos
    and al, ah ;al tiene el "si no es 0" y ah tiene el "si es ']'", y si ambos son correctos, ignoramos el salto y seguimos
    jz %%exit
    mov r10, rsi ;vamos al puntero de la celda
    shl r10, 3
    add r10, 1 ;revisamos el lugar de al lado
    mov esi, [cell+r10] ;movemos el puntero de instrucción para hacer el salto
    and rsi, -1 ;limitamos a 32 bits
%%exit: ;salimos
%endmacro
