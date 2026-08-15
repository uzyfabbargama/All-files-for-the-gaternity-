; macros.inc - Todas las macros del intérprete

; ============================================
; GENERADOR DE CONSTANTES
; ============================================
%macro constans_generator 1
    %assign i 0
    %rep 8
        %define %1%i i
        %assign i i+1
    %endrep
%endmacro

; ============================================
; CONTROLADORES DE RSI (Puntero a código)
; ============================================
%macro rsicontroller 1
    setz r9b
    and r9, 1
    neg r9
    and r9, %1
    add rsi, r9
%endmacro

; ============================================
; CONTROLADORES DE CELDA
; ============================================
%macro addcontroller 1
    test r10, r10
    jz %%setreset
    jmp %%normal
    %%setreset:
        mov r10, %1
    %%normal:
        mov al, [cell+rbx]
        add al, r10b
        mov [cell+rbx], al
%endmacro

%macro subcontroller 1
    test r10, r10
    jz %%setreset
    jmp %%normal
    %%setreset:
        mov r10, %1
    %%normal:
        mov al, [cell+rbx]
        sub al, r10b
        mov [cell+rbx], al
%endmacro

%macro leftcontroller 1
    test r10, r10
    setnz r9b
    neg r9
    sub r10, %1
    and r10, r9
    shl r10, 3      ; Multiplicar por 8 (tamaño de celda)
    sub rbx, r10
%endmacro

%macro rightcontroller 1
    test r10, r10
    setnz r9b
    neg r9
    add r10, %1
    and r10, r9
    shl r10, 3      ; Multiplicar por 8 (tamaño de celda)
    add rbx, r10
%endmacro

; ============================================
; DETECTOR DE PATRONES (8 bytes a la vez)
; ============================================
%macro detectar_plus 0
    xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "+"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 1
    shr r8, 5
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        addcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_minus 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "-"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        subcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_left 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, "<"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        leftcontroller i
        %assign i i+1
    %endrep
%endmacro

%macro detectar_right 0
	xor r10, r10
    mov rax, [font_code+rsi]
    ror rax, 8
    %rep 8
        cmp al, ">"
        setz r9b
        and r9, 1
        mov rcx, r9
        neg r9
        and al, r9b
        xor r8b, al
        shl r8, cl
        shr rax, 8
    %endrep
    shr r8, 6
    %assign i 1
    %rep 8
        mov rax, r8
        shr rax, i
        cmp rax, 0
        rsicontroller i
        rightcontroller i
        %assign i i+1
    %endrep
%endmacro

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

; ============================================
; ENTRADA / SALIDA
; ============================================
%macro output_char 0
    cmp byte [font_code+rsi], '.'
    jne %%exit
    
    push rsi
    push rbx
    push rax
    
    movzx rdi, byte [cell+rbx]
    mov rax, 1
    sub rsp, 8          ; Alinear a 16 bytes
    mov [rsp], dil
    mov rsi, rsp
    mov rdx, 1
    syscall
    add rsp, 8
    
    pop rax
    pop rbx
    pop rsi
%%exit:
%endmacro

%macro input_char 0
    cmp byte [font_code+rsi], ','
    jne %%exit
    push rsi
    push rbx
    
    mov rax, 0
    mov rdi, 0
    sub rsp, 8          ; Alinear stack
    mov rsi, rsp
    mov rdx, 1
    syscall
    movzx rcx, byte [rsp]  ; Usar RCX como temporal
    add rsp, 8
    
    mov [cell+rbx], cl     ; Guardar en la celda actual (RBX sigue intacto)
    
    pop rbx
    pop rsi
%%exit:
%endmacro
; ============================================
; DEBUG DE RESGISTROS
; ============================================
%macro debug_print_rsi 0
;    push rax
;    push rdi
;    push rsi
;    push rdx
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, debug_buffer
;    mov rdx, 1
;    syscall
;    pop rdx
;    pop rsi
;    pop rdi
;    pop rax
nop
%endmacro
%macro debug_running 0
; Debug: imprimir un carácter para saber que llegamos
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, msg_debug
;    mov rdx, 1
;    syscall
nop
%endmacro

%macro debug_output 0
;	; Debug: imprimir un carácter
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, msg_dot
;    mov rdx, 1
;    syscall
nop
%endmacro
