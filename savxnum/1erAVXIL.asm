; --- 1. DEFINICIÓN DE MACROS (Siempre arriba de todo) ---
%macro super_mov 2
    vmovdqu %1, %2
%endmacro

%macro super_add 3
    vpaddw %3, %1, %2
%endmacro

%macro finish 0
    mov rax, 60         ; syscall para exit
    xor rdi, rdi        ; status 0
    syscall
%endmacro

; --- 2. DATOS ALINEADOS ---
section .data
    align 32
    variables_presion dw 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
    align 32
    gota_incremento   dw 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

; --- 3. CÓDIGO ---
section .text
    global _start

_start:
    ; 1. Cargar Presión Actual (Usamos yword para asegurar 256 bits)
    super_mov ymm0, [variables_presion]
    
    ; 2. Cargar Incrementos
    super_mov ymm1, [gota_incremento]
    
    ; 3. Sumar Masivamente [ymm2 = ymm0 + ymm1]
    super_add ymm2, ymm0, ymm1
    
    ; 4. Guardar Resultado de Vuelta
    super_mov [variables_presion], ymm2   

parar_aqui:
    finish