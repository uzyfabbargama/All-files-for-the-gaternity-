    %macro mem_mov 2;Origen, Destino
        mov r11, %2   ; R11 actúa como nuestro "registro link"
        mov %1, r11
    %endmacro
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
;    // %measer 3; 1 = bit, 2 = zone, 3 = range min
;    //     mov rax, %2
;    //     shr rax %1
;    //     and rax, 0xFF ;Tomamos 8 bits
;    //     and r9, rax

    %macro elsecond 2
    mov rax, %2         ;Acceder al contexto
    shr rax, %1         ;Ubicación
    and rax, 1          ;Filtro and
    xor r9, rax         ;conexión inversa
    xor r9, 1           ;negación
    %endmacro
    
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
    
    %macro xorid 0
    	mov r9, 32
    	xor r9b,[INPUT + 1]
    	setz r9b
    	jz %%xip
    	jmp %%no
    	%%xip:
        	mov r11, r14                ; r11 = ID anterior
        	xor r9, 1					; 1 = 0, 0 = 1 
        	sub r9, 1					; flip r9 (1→-1, 0→0)
        	xor r11b, [INPUT + r13]     ; r11 = (anterior XOR byte)
        	and r11, r9                 ; aplica máscara condicional
        	add r9, 2                   ; si es -1 es true, si es 0, es 2
        	and r9, 1                   ; si es 1, es 1, si es 2 es 0
        	mov rcx, r9                 ; sólo rcx, acepta shift condicional
        	shl r11, cl                 ; shift condicional (1 bit si r9=1)
           ; Verificar si es espacio
        	cmp byte [INPUT + r13], ' '
        	jne %%update_id
    
        
        	
        jmp %%no
    
        %%update_id:
        ; Es espacio: guardar el ID ACTUAL (r11)
        	and r11, 0x0f_ffff          ; limitamos a 1MB
        	shl r11, 3                  ; *8 para alinear
        	mov [NameSpace + r11], r11d ; guardamos el ID en la lista
        	add r14, r11                ; actualizar ID solo si NO es espacio
    		jmp %%end
        %%no:
            nop
            xor r9, r9 ;siempre 0
        %%end:
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
    %macro skip 2 ;bit, r15
    mov r9, %2 ;toma el mapa
    shr r9, %1 ;verifica el bit
    and r9, 0x1;aisla el bit
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
        and r9, 0x1 ; 1 = 1, 0 = 0
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
;xor: objetivos: 1 = FFFF_FFFF_FFFF_FFFF, 0 = FFFF_FFFF_FFFF_FFFF
%macro andcond 3 ;poscond, valor, donde
    shr r9, %1  ; vamos a la posición
    and r9, 0x1 ; tomamos un sólo bit
    add r9, 1   ; 1 = 10, 0 = 1
    and r9, 0   ; 1 = 0, 0 = 0
    sub r9, 1   ; 1 = FFFF_FFFF_FFFF_FFFF, 0 = FFFF_FFFF_FFFF_FFFF
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
