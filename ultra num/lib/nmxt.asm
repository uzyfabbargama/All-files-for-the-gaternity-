 %define ID_PARTE_DECIMAL 1428860  ;parte_decimal: 
 %define ID_SEP           748 
 ;nos ahorramos el :: 
 %define ID_FINAL         232  ; El ",," 
%macro xif_check 3 ; ID, Cantidad, Etiqueta_Si_Falla
    xor r8, r8
    %assign i 0
    %rep %2
        movzx rax, byte [rdi + rsi + i]
        shl r8, 1
        xor r8, rax ; Usamos tu lógica de trituración
        %assign i i+1
    %endrep
    cmp r8, %1
    jne %3          ; Si no es la palabra clave, salta a la siguiente comprobación
    add rsi, %2     ; SI ES la palabra, saltamos esos bytes de golpe
    xor %3, %3      ; Limpiamos el acumulador para el número que viene
 %endmacro
 %macro mul_10 1 ;MACRO ACTUALIZADA PARA 64 BITS + reg
    ; Solo multiplicamos si r9 es 1
    test r9, r9
    jz %%skip_mul
    imul %1, 10
%%skip_mul:
%endmacro
 %macro suma_cond 2 ;%1 valor, %2, el registro
    xor rax, rax            
    mov rax, r9         
    neg rax             
    and rax, %1         
    add %2, rax        
%endmacro

 %macro if_num 3 
    ; 1. ¿Es el carácter actual (dl) igual al dígito buscado?
    cmp dl, %2          
    
    ; 2. r9 se vuelve 1 si es igual, 0 si no. Sin arrastrar estados previos.
    setz r9b
    movzx r9, r9b
    
    ; 3. Si r9 es 1, operamos sobre r12. Si es 0, las macros no hacen nada.
    mul_10 %3 ;(listo
    suma_cond %1, %3    ; %1 es el valor numérico (0-9) (listo)
 %endmacro
 %capturar_numero 1
 %%ciclo:
 	movzx rdx, byte [rdi + rsi]
 	; Verificar si es dígito (ASCII 48-57)
    cmp dl, '0'
    jl %%fin
    cmp dl, '9'
    jg %%fin 
    if_num 1, "1", %1 ;(listo)
    if_num 2, "2", %1
    if_num 3, "3", %1
    if_num 4, "4", %1
    if_num 5, "5", %1
    if_num 6, "6", %1
    if_num 7, "7", %1 
    if_num 8, "8", %1
    if_num 9, "9", %1
    if_num 0, "0", %1
    inc rsi
    jmp %%ciclo
%endmacro
 
 
 _nmxt_parser:
    xor rcx, rcx  ; para las masks
    mov r10, rsi  ; rsi entra con la dirección de 'self.mente' desde Python
    xor rsi, rsi  ; Limpiamos rsi para usarlo como índice del string (RDI)
    xor r13, r13  ; bits entero
    xor r15, r15  ; Valor SEP
    xor r14, r14  ; bits Decimal
    lea rbx, [rel bucle_principal]    ; Usamos RBX para el salto
    jmp rbx
bucle_principal:
    movzx rdx, byte [rdi + rsi] 
    test dl, dl                 
    jz total_exit
    
    ; 1. ¿Es "parte_entera:"?
    xif_check ID_PARTE_ENTERA, 13, .check_dec
    capturar_numero r13
    jmp bucle_principal
.check_dec:
    xif_check ID_PARTE_DECIMAL, 14, .check_sep
    capturar_numero r14
    jmp bucle_principal
.check_sep:
    xif_check ID_PARTE_SEP, 3, .check_final
    capturar_número r15
    jmp bucle_principal
.check_final:
    xif_check ID_PARTE_FINAL, 2, .inc_and_loop
    jmp bucle_principal
    ret
section .note.GNU-stack noalloc noexec nowrite progbits
.inc_and_loop:
    inc rsi
    jmp procesar
procesar:
	;1. Obtener los últimos bits de r14
    mov rcx, r14 	;parte frac
    mov rax, 1  	; rax = 1
    shl rax, cl		: Creamos la máscara dinámica
    dec rax
    ;2. Extraer parte decimal (r14 final)
    mov r14, r15	; Extraer la fracción de r15
    and r14, rax	; r14 es ahora el .decimal
    
    ;3. Extraer parte entera (r13 final)
    mov r13, r15
    shr r13, cl		; r13 = el 11. entero
    mov [r10], r13	; Guardamos parte entera
    add r10, 16		; Movemos el puntero al siguiente sot
	jmp bucle_principal ;¡A por más números!
