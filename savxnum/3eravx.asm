; --- Macros ---
%macro super_mov 2
    vmovdqa %1, %2
%endmacro

%macro super_add 3
    vpaddw %3, %1, %2
%endmacro

section .data
    align 32
    variables dw 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10
    align 32
    incremento dw 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1

section .text
    global _start

_start:
    super_mov ymm0, [variables]
    super_mov ymm1, [incremento]
    super_add ymm0, ymm1, ymm2    ; ymm2 = ymm0 + ymm1

.parar:                           ; Nuestra zona de seguridad
    mov rax, 60
    xor rdi, rdi
    syscall