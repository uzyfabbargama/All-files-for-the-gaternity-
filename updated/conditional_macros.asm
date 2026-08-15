    %macro FIRSTcond 2 ;KW, Contexto
    mov rax, %2     ;Contexto
    shr rax, %1     ;tipo KW
    and rax, 1      ;Filtro and
    mov r9, rax     ;Iniciar
    %endmacro
    ; %1 = Bit a testear
	; %2 = Registro donde mirar (r15 para keywords, r8 para números)
    %macro cond 2
    mov rax, %2     ;Accedemos al registro que TÚ decidas
    shr rax, %1     ;Movemos el bit al final
    and rax, 1      ;Filtramos
    and r9, rax     ;Cascada de éxito en r9
    %endmacro


    %macro elsecond 2
    mov rax, %2         ;Acceder al contexto
    shr rax, %1         ;Ubicación
    and rax, 1          ;Filtro and
    xor r9, rax         ;conexión inversa
    and r9, 1           ;booleano mode
    %endmacro
    %macro is_depth 3
    mov rax, %2         ;Acceder al contexto
    shr rax, %1         ;ubicación
    and rax, 8          ;filtro
    cmp rax, %3         ;verificar profundidad
    setnz r9b           ;si no es 0, R9 = 1
    movzx r9, r9b       ;movextend
    %endmacro
    %macro elseif
    and r9, 1
    xor r9, 1
    %endmacro
    %macro update_depth 2
    shl r9, %1         ;ubicación
    dec %2, r9         ;restamos 1 en la ubicación correspondiente
    shr r9, %1         ;volvemos a la normalidad
    and r9, 1          ;volvemos a booleano
    %endmacro
    %macro type_ctrl 1
    mov r11, use_ctrl
    add r11, %1
    xor r9, 1
    sub r9, 1
    and r11, r9
    jnz %%si
    jmp %%no
    %%si:
        mov rax, [r14]
        shr rax, 20
        and rax, 0xFFF
        mov rax, r11
        mov [r14], rax
    %%no:
        nop
 	%macro xif 3 ; ID, Cantidad, bit
        %%normal:	
    	xor r8, r8
    	%assign i 0
    	%rep %2
        	movzx rax, byte [INPUT +r13 + i]
        	xor r8, rax ; Usamos tu lógica de trituración
        	shl r8, 1
        	%assign i i+1
    	%endrep
    	xor r8, %1
    	setz r9b
    	movzx r9, r9b 	; Para limpiar
        shl r9, %3
        mov rax, r9
        test r9, r9
    	jz %%no       	; Si no es la palabra clave, salta a la siguiente comprobación
    	add r13, %2     ; SI ES la palabra, saltamos esos bytes de golpe
    	add r13, 1      ; Para saltear el espacio
        %%no:
            ;inc r13
            nop
 	%endmacro
    %macro prev 2
        xor r9, r9          ;Para condición
        mov dl, [INPUT+r13-1]     ;el INPUT
        movzx r9, dl        ;Para comparar
        cmp r9, %2         ;INPUT vs valor_real
        setz r9b            ;si era 0 le da 1
        and r9, 0x1         ;borra toda la basura
        shl r9, %1          ;desplazamos (si es 0 seguirá siendo 0, sino, será la máscara)
        or rax, r9          ;le agregamos rax
        shr r9, %1          ;Para que vuelva a ser booleano
    %endmacro
    %macro si 2 			;destino, valor
        xor r9, r9          ;Para condición
        mov dl, [INPUT+r13] ;el INPUT
        movzx r9, dl        ;Para comparar
        cmp r9, %2          ;INPUT vs valor_real
        setz r9b            ;si era 0 le da 1
        and r9, 0x1         ;borra toda la basura
        shl r9, %1          ;desplazamos (si es 0 seguirá siendo 0, sino, será la máscara)
        or rax, r9          ;le agregamos rax
        setnz r9b           ;Para que vuelva a ser booleano
    %endmacro
    %macro si_nop 0
    	cmp byte [INPUT + r13], 0
     	je %%exit
    	jmp %%seguir
    	%%exit:
    	; N-Lang muere cuando recibe un 0
        	mov rax, 60         ; syscall exit
        	xor rdi, rdi        ; código 0
        	syscall
        %%seguir:
        	nop
    %endmacro
    %macro count_in 1
        add %1, rax
    %endmacro
    %macro do_in 1
        xor %1, rax
    %endmacro
    
    %macro is_kw 2
        mov r9, r15     ;tomamos el mapa
        shr r9, %1      ;buscamos la keyword
        and r9, 1       ;tomamos un bit
        xor r9, 1       ;1 = 0, 0 = 1
        sub r9, 1       ;1 = -1, 0 = 0
        and r9, %2      ;1 = %2, 0 = 0
        mov r8, r9      ;1 = keyword, 0 = 0
    %endmacro
    %macro is_class 3
        mov r9, r15     ;tomamos el mapa
        shr r9, %1      ;buscamos keyword
        and r9, 1       ;tomamos un bit
        xor r9, 1       ;1 = 0, 0 = 1
        sub r9, 1       ;1 = -1, 0 = 0
        and r9, %2      ;1 = %2, 0 = 0
        mov r8, r9      ;1 = %2, 0 = 0
        mov r9, r15     ;tomamos otro mapa
        shr r9, %3      ;otra keyword
        and r9, 1       ;tomar bit
        xor r9, 1       ;invertir
        sub r9, 1       ;1 = -1, 0 = 0
        and r9, %2      ;1 = %2, 0 = 0
        sub r8, %2      ;para en el futuro, anular la definición de la CLASS
    %endmacro
;objetivo: 1 = FFFF_FFFF_FFFF_FFFF, 0 = 0
%macro addcond 3 ; posición condición, valor, donde
    mov r9, r15 ; mapa
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    xor r9, 1   ; invertimos el bit
    sub r9, 1   ; 1 = FFF...., 0 = 0
    and r9, %2  ; 1 = self, 0 = none
    add %3, %2  ; sumamos
    and r9, 0x1 ; volvemos a booleano 
%endmacro

%macro subcond 3 ;posición condición, valor, donde
    mov r9, r15 ; mapa
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    xor r9, 1   ; invertimos el bit
    sub r9, 1   ; 1 = FFF...., 0 = 0
    and r9, %2  ; 1 = self, 0 = none
    sub %3, %2  ; restamos
    and r9, 0x1 ; volvemos a booleano 
%endmacro
%macro orcond 3 ;posición condición, valor, donde
    mov r9, r15 ; mapa
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    xor r9, 1   ; invertimos el bit
    sub r9, 1   ; 1 = FFF...., 0 = 0
    and r9, %2  ; 1 = self, 0 = none
    or %3, %2  ; restamos
    and r9, 0x1 ; volvemos a booleano 
%endmacro

;xor: objetivos: 1 = FFFF_FFFF_FFFF_FFFF, 0 = FFFF_FFFF_FFFF_FFFF
%macro andcond 3 ;poscond, valor, donde
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    sub r9, 1   ; 1 = 0, 0 = -1
    or %2, r9   ; 1 = self, 0 = -1
    and r9, %2  ; 1 = self, 0 = none
    and %3, %2  ; and
    and r9, 0x1 ; volvemos a booleano 
%endmacro
;and: objetivos: 1 = 0, 0 = FFFF_FFFF_FFFF_FFFF
%macro xorcond 3 ;poscond, valor, donde
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    sub r9, 1   ; 1 = 0, 0 = FFFF_FFFF_FFFF_FFFF
    and r9, %2  ; 1 = self, 0 = none
    xor %3, %2  ; xor
    and r9, 0x1 ; volvemos a booleano 
%endmacro
%macro cleare 0
	sub r9, 1 ;1 = 0, 0 = -1
	and r15, r9 ;es mucho mejor
%endmacro
