 %macro mem_mov 2;Origen, Destino
        mov r11, %2   ; R11 actúa como nuestro "registro link"
        mov %1, r11
    %endmacro
    %include "conditional_macros.asm"
    %macro free_block 1
        mov rax, 11        ; syscall munmap
        mov rdi, %1        ; dirección a liberar
        mov rsi, 4096      ; tamaño de página
        syscall
    %endmacro
    %macro xorid 0 ;condiciones de parada
        mov r11, r14
        %%inicio:
        	add r11, r14                ; r11 = ID anterior
        	and r9, 1                   ; es 1 o 0 y depende de las macros anteriores, haciendo un swich branchless poe aritmética 
        	sub r9, 1					; flip r9 (1→0, 0→-1)
        	xor r11b, [INPUT + r13]     ; r11 = (anterior XOR byte)
        	and r11, r9                 ; aplica máscara condicional
        	add r9, 2                   ; si es -1 es true, si es 0, es 2
        	and r9, 1                   ; si es 1, es 1, si es 2 es 0
        	mov rcx, r9                 ; sólo rcx, acepta shift condicional
        	shl r11, cl                 ; shift condicional (1 bit si r9=1)
        	add r14, r11                ; cerramos el círculo
           ; Verificar si alguna condición de salida
           	inc r13, 1 ;sumamos
           	si 0, "(" ;comparamos
           	mov r8, r9                  ;guardar condición
           	si 0, "{"
           	or r8, r9
           	si 0, "["
           	or r8, r9
           	si 0, "]"
           	or r8, r9
           	si 0, " "
           	or r8, r9
           	dec r13 ;volvemos
           	test r9, r9
        	jz %%inicio ;saltamos
            jmp %%update_id
        %%update_id:
        ; Es espacio: guardar el ID ACTUAL (r11)
        
            is_kw KW_VAR, use_var
            is_kw KW_CTRL, use_ctrl
            is_class KW_CLASS, use_class, maked_CLASS
            push r9
            Firstcond KW_maked_CLASS, r15
            test r9, r9
            jnz %%UI_class_object
            pop r9
            shl r9, 20
            sub r9, 1
        	and r11, r9                 ; limitamos a 20 bits
        	shl r8, 20                  ; salteamos 20 bits para meter el tipo de keyword
        	add r11, r8                 ; metemos el tipo de keyword
        	shl r11, 4                  ; *16 bytes por N-Object
        	add r14, r11                ; actualizar ID solo si NO es espacio
        	mov r8, [NameSpace + r14]   ; verificamos que esté vacío
        	and r8, 0xFFFFF
        	test r8, r8
        	jnz %%error
        	mov [NameSpace + r14], r11d ; guardamos el ID en la lista
    		jmp %%no
        %%error:
            ;print;("Variable ya definida, error") (falta definir macro para imprimir)
            jmp %%no
    	%%UI_class_object:
    	    shl r9, 20
    	    sub r9, 1
    	    and r11, r9
    	    shl r8, 20 					;para no corromper xorid
    	    add r11, r8
    	    shl r11, 5					;32 bytes por N-Object Local
    	    add r14, r11
    	    mov r8, [RBX + r14+12]      ; verificamos que esté vacío
    	    and r8, 0xFFFFF
    	    test r8, r8
    	    jnz %%error
    	    mov [RBX + r14+12], r11d    ;movemos el objeto local 12 bytes (4 son el ID local, y 8 es el valor de 64 bits)
    	    jmp %%no
        %%no:
            nop
    %endmacro
%macro verif_string_leak 0                      ; macro para verificar texto
    mov r8w, [RBX + R14]                        ; tomamos 4 bytes del ID del objeto local
    shr r8w, 20                                 ; desplazamos 20 para obtener los 12 bits para saber si es modo string
    and r8w 0xFFF                               ; aislamos esos 12 bits
    xor r8w, use_string                         ; comparamos con xor, si es 0, es correcto
    test r8w, r8w                               ; testeamos si es 0
    jz %%verif_string                           ; saltamos a verificar el string, para la transmisión
    jmp %%no                                    ; sino, no hacemos nada
    %%verif_string:                             ; modo para verificar el string
        mov r8, [RBX + R14 + 4]                 ; nos movemos dentro del objeto local para obtener la dirección de memoria
        test r8, r8	    						; testeamos
        jnz %%move_dir                          ; sino da 0, vamos a move_dir
        jmp %%no                                ; sino no hacemos nada
   %%move_dir:
        mov rax, [RBX + R14 + 12 + 4 + 2 + 2]   ; vamos a la dirección de memoria del texto
        test rax, rax                           ; comparamos que no sea 0
        push r13                                ; cargamos r13 a la pila por las dudas
        push r8                                 ; cargamos r8 también
        mov r13, 0                              ; reseteamos r13 (mov no afecta ZF)
        jnz %%looptring                         ; si no es 0 entramos aquí
        pop r13                                 ; si no, devolver r13
        pop r8                                  ; también r8
        jmp %%no                                ; saltamos a no hacer nada
   %%continuar:                                 ; etiqueta para continuar (aquí entra looptring)
        pop r8                                  ; lo sacamos de la pila a r8 nuevamente
        pop r13                                 ; lo sacamos de la pila a r13 también
        jmp %%no                                ; si era 0, no hacmoes nada
        free_block [rax]                       ; colocar aquí una macro para liberar la memoria
        mov rax, r8                             ; reemplazo de punteros
        mov [RBX + R14 + 12 + 4 + 2 + 2], rax   ; movemos una dirección predeterminada
   %%looptring:
        mov r8, [rax+r13]                       ; nos movemos según el puntero dentro de RAX (la dirección que nos dió el kernel)
        xor r8, 0                               ; verificamos que sea 0
        setnz r9b                               ; sino es 0, r9 = 1
        movzx r9, r9b                           ; movemos ese resultado a r9
        shl r9, 3                               ; si r9 es 1, se convierte en 8, sino en 0
        add r13, r9                             ; sumamos el valor de r8 (8 o 0) a r13 (nuestro puntero de bytes)
        pop r8                                  ; alto riesgo, jeje (aprovechamos el poder LIFO)
        mem_mov [r8], [rax+r13]                 ; movemos el contenido de r8 (la dirección origanal) a rax (la nueva) usando r13 como puntero
        push r8                                 ; no olvidar esto
        test r9, r9
        jz %%looptring
        jmp %%continuar
   %%no:
        nop
%endmacro        
    ; --- Macros Aritméticas ---
 %macro mul_10 1 
    test r9, r9
    jz %%skip_mul
    imul %1, 10
%%skip_mul:
%endmacro

%macro suma_cond 2 ;1, reg 
    xor rax, rax            
    mov rax, r9         
    neg rax             
    and rax, %1         
    add %2, rax        
%endmacro

%macro if_num 3 
    cmp dl, %2          
    setz r9b
    movzx r9, r9b
    mul_10 %3 
    suma_cond %1, %3    
%endmacro

; --- Macro Capturar Número (Corregida) ---
%macro capturar_numero 1
%%ciclo:
    movzx rdx, byte [INPUT + r13]
    cmp dl, '0'
    jl %%fin
    cmp dl, '9'
    jg %%fin
    
    if_num 1, '1', %1
    if_num 2, '2', %1
    if_num 3, '3', %1
    if_num 4, '4', %1
    if_num 5, '5', %1
    if_num 6, '6', %1
    if_num 7, '7', %1 
    if_num 8, '8', %1
    if_num 9, '9', %1
    if_num 0, '0', %1
    if_num 0, 32, %1
    inc r13
    jmp %%ciclo
%%fin:
%endmacro

    %macro sumar_indice 0
        add r13, r9         ;agregar 1 a RSI, sólo si r9 es 1
        %endmacro
    %macro skip 0 ;saltea de forma simple
    and r9, 0x1
    add r13, r9;avanza el puntero de bytes, sólo si r9 es 1
    %endmacro
    %macro UPDATE_KW 2 
        mov r9, r15      ;obtener el mapa completo
        xor r9, %2        ;Si es 0 no lo destruye, si es 1, si    
        shr r9, %1       ;desplazado r9 para el tipo de keyword
        and r9, 0x1      ;toma un solo bit
        xor r15, r9     ;Reinicia estado de 1 → 0
        ;Si condición: 0 + keyword 1 = keyword 1
        ;Si condición: 1 + keyword 1 = keyword 0
    %endmacro
    %macro detect 3 ; ID, Cantidad, value
        %%normal:	
    	xor r8, r8
    	%assign i 0
    	%rep %2
        	movzx rax, byte [INPUT + r13 + i]
        	xor r8, rax ; Usamos tu lógica de trituración
        	shl r8, 1
        	%assign i i+1
    	%endrep
    	xor r8, %1
    	setz r9b
    	mov r9, r9b 	; Para limpiar
        add r9, %3      ; Para la dirección
        mov rax, r9
    	jnz %%no       	; Si no es la palabra clave, salta a la siguiente comprobación
    	add r13, %2     ; SI ES la palabra, saltamos esos bytes de golpe
        %%no:	
 	%endmacro 
    dec r9 ; 1 = 0, 0 = 0xF...
                xor r9, 0xFFFF ; 0 = 0xf...0000 1 = 0xFFFF
                and r9, 0xFFFF ; 0 = 0, 1 = 0xFFFF (Limita a 16 bits sólo si hay paréntesis y es VAR)
                and r12, r9 ; convierte r12 en 16 bits
    %macro convert16b 0
        dec r9 ; 1 = 0, 0 = 0xF...
        xor r9, 0xFFFF ; 0 = 0xf...0000 1 = 0xFFFF
        and r9, 0xFFFF ; 0 = 0, 1 = 0xFFFF (Limita a 16 bits sólo si hay paréntesis y es VAR)
        and r12, r9 ; convierte r12 en 16 bits
        and r9, 0x1 ; 0 = 0, 1 = 1
    %endmacro
    %macro convert1b 0
        dec r9      ; 1 = 0, 0 = 0xF...
        xor r9, 0x1 ; 1 = 1, 0 = 0xF..E
        and r9, 0x1 ; 1 = 1, 0 = 0
        and r12, r9 ; 1 = 1, 0 = 0
        ;este es el legendario: bool(int) de Python en 4 ciclos de reloj, jajaja
        ;n = 1/true, 0 = false/0
    %endmacro
    %macro set_threshold 0
        xor r12, 0xFFFF
        add r12, 1
    %endmacro
    %macro ready 2
    shl r9, %1
    or %2, r9
    shr r9, %1
    and r9, 1
    %endmacro
%macro expanse 0
    push r10        ; Lo movemos
    mov rax, 9       ; Número de Syscall
    xor rdi, rdi    ;(El kernel elige la dirección de memoria)
    mov rsi, 4096   ;1 página = 4 KB
    mov rdx, 3      ; prot_read | prot_write
    mov r10, 34     ;r10 = flags (map_private)| map_anonymous
    mov r8, -1      ; r8 = file_descriptor (-1 porque no es un archivo)
    mov r9, 0       ; r9 = offset 0
    syscall         ; ¡Invocamos al kernel!
    mov rbx, rax    ; ahora rbx tiene la dirección de memoria
    pop r10         ; Lo recuperamos
%endmacro
%macro create_class 0
    push r10,
    mov rax, 9
    xor rdi, rdi
    mov rsi, 1
    shl rsi, 25
    mov r10, 34
    mov r8, -1
    mov r9, 0
    syscall
    mov rbx, rax
    pop r10
%endmacro
;objetico 1 = FFFF_FFFF_FFFF_FFFF, 0 = 1
;%macro mulcond 3 ;posición condición, valor, donde
;    shr r9, %1  ; vamos a la posición
;    and r9, 0x1 ; tomamos un sólo bit
;    xor r9, 1
;    add r9, 9  ; 1 = 1010, 0 = 1001
;    and r9, 4  ; 1 = 0, 0 = 100
;    shr r9, 1  ; 1 = 0, 0 = 10 ¡al fin, ahora el estado true < false y false es mayor por dos puntos!
;    sub r9, 1   ; 1 = FFFF_FFFF_FFFF_FFFF, 0 = 1 (si es false, se multiplica por 1, si es true, por el número)
;    and r9, %2  ; 1 = self, 0 = none
;    mul %3, %2  ; multiplicamos
;    and r9, 0x1 ; volvemos a booleano 
;%endmacro
;%macro divcond 3 ;poscond, valor, donde
;    shr r9, %1  ; vamos a la posición
;    and r9, 0x1 ; tomamos un sólo bit
;    add r9, 9  ; 1 = 1010, 0 = 1001
;    and r9, 4  ; 1 = 0, 0 = 100
;    shr r9, 1  ; 1 = 0, 0 = 10 ¡al fin, ahora el estado true < false y false es mayor por dos puntos!
;    sub r9, 1   ; 1 = FFFF_FFFF_FFFF_FFFF, 0 = 1 (si es false, se multiplica por 1, si es true, por el número)
;    and r9, %2  ; 1 = self, 0 = none
;    div %3, %2  ; dividimos
;    and r9, 0x1 ; volvemos a booleano 
;%endmacro 
