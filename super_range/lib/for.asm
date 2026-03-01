section .text
global _for_parser
%define ID_START 2688 ;sta:
%define ID_STEP 2720 ;ste:
%define ID_STOP 2800 ;sto:
; --- 1. Macro de verificación de firmas ---
%macro xif_check 3 ; ID, Cantidad, Etiqueta_Si_Falla
    xor r8, r8
    %assign i 0
    %rep %2
        movzx rax, byte [rdi + rsi + i]
        xor r8, rax ; Usamos tu lógica de trituración
        shl r8, 1
        %assign i i+1
    %endrep
    cmp r8, %1
    jne %3          ; Si no es la palabra clave, salta a la siguiente comprobación
    add rsi, %2     ; SI ES la palabra, saltamos esos bytes de golpe
 %endmacro
 ; --- 2. Macros Aritméticas ---
 %macro mul_10 1 
    test r9, r9
    jz %%skip_mul
    imul %1, 10
%%skip_mul:
%endmacro

%macro suma_cond 2 
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

; --- 3. Macro Capturar Número (Corregida) ---
%macro capturar_numero 1
%%ciclo:
    movzx rdx, byte [rdi + rsi]
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
    inc rsi
    jmp %%ciclo
%%fin:
%endmacro
;--- 4. Analizer ---
%macro analizer 1
	mov r9, %1
	shr r9, 32 	;movemos 32 bits
	and r9, 0x1 ;filtro and
	xor r9, 0x1	;inversor
%endmacro
; --- MOTOR PRINCIPAL ---
_for_parser:
	mov r10, rsi ; r10 = Puntero (Python)
	xor rsi, rsi ; rsi = índice del string de entrada
	xor r13, r13 ; Valor start
	xor r14, r14 ; Valor step
	xor r15, r15 ; Valor stop
bucle_principal:
	movzx rdx, byte [rdi + rsi]
	test dl, dl
	jz total_exit
	xif_check ID_START, 5, .check_sto
	capturar_numero r13 ;guardar start
	jmp bucle_principal
	
.check_sto:
	xif_check ID_STOP, 5, .check_ste
	capturar_numero r15
	jmp bucle_principal
.check_ste:
	xif_check ID_STEP, 5, bucle_principal
	capturar_numero r14
	jmp .res
.res:
	;Límite 32 bits
	mov r11, 0xFFFF_FFFF ;guardamos una máscara de 32 bits
	;Complemento a 2 (r11 xor stop) + 1
	xor r11, r15
	inc r11
	;Start x Step
	add r13, r14
	jmp .sum
.sum:
	analizer r11 ;toma los 32 bits de r11
	test r9, r9 ;si es 0
	jz total_exit
	; --- INYECCIÓN A LA MENTE ---
    mov [r10], r13    ; Guardamos el valor actual (r13) en la dirección de r10
    add r10, 8         ; Avanzamos 8 bytes (tamaño de un long long) en la RAM
    ; ----------------------------
	add r11, r14 ;suma mientras r9 sea 1
	jmp .sum
total_exit:
	ret
section .note.GNU-stack noalloc noexec nowrite progbits
