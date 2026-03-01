section .text
global _nmxt_parser

; --- IDs y Constantes ---
%define ID_PARTE_ENTERA  536
%define ID_PARTE_DECIMAL 1202
%define ID_SEP           748
%define ID_FINAL         452

; --- 1. Macro de verificación de firmas ---
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
    
    inc rsi
    jmp %%ciclo
%%fin:
%endmacro

; --- MOTOR PRINCIPAL ---
_nmxt_parser:
    mov r10, rsi         ; r10 = Puntero a la Mente (Python)
    xor rsi, rsi         ; rsi = Índice del string de entrada
    xor r13, r13         ; Bits parte entera
    xor r14, r14         ; Bits decimal
    xor r15, r15         ; Valor total (sep)

bucle_principal:
    movzx rdx, byte [rdi + rsi]
    test dl, dl
    jz total_exit

    ; Chequeos de firma
    xif_check ID_PARTE_ENTERA, 3, .check_dec
    capturar_numero r13
    jmp bucle_principal

.check_dec:
    xif_check ID_PARTE_DECIMAL, 4, .check_sep
    capturar_numero r14
    jmp bucle_principal

.check_sep:
    xif_check ID_SEP, 3, .check_final
    capturar_numero r15
    jmp bucle_principal

.check_final:
    xif_check ID_FINAL, 3, .inc_and_loop
    jmp procesar

.inc_and_loop:
    inc rsi
    jmp bucle_principal

procesar:
    ; Aritmética de punto fijo (nmxt)
    mov rcx, r14         ; Cantidad de bits decimales a RCX
    mov rax, 1
    shl rax, cl          ; Máscara = 1 << bits_dec
    dec rax              ; Máscara = (1 << bits_dec) - 1
    
    mov r11, r15         ; Copiamos valor total a R11
    and r11, rax         ; r11 = PARTE DECIMAL extraída
    
    mov r12, r15         ; Copiamos valor total a R12
    shr r12, cl          ; r12 = PARTE ENTERA extraída
    
    ; Inyectamos en la Mente (r10)
    mov [r10], r12       ; Guardamos entero
    mov [r10 + 8], r11   ; Guardamos decimal
    add r10, 16          ; Avanzamos 16 bytes para el próximo número
    
    ; Reset de registros para el siguiente número
    xor r13, r13
    xor r14, r14
    xor r15, r15
    jmp bucle_principal

total_exit:
    ret

section .note.GNU-stack noalloc noexec nowrite progbits
