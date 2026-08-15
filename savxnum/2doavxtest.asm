section .text
    global _start

_start:
    ; Intentamos una instrucción AVX que no use memoria
    ; Limpiar ymm0 (esto no debería fallar si AVX es legal)
    vxorps ymm0, ymm0, ymm0
    
    ; Si llegamos aquí, AVX funciona. 
    ; Salida
    jmp .parar
.parar:
    mov rax, 60
    xor rdi, rdi
    syscall