section .data
    align 16 ; SSE usa 16 bytes
    variables dw 10, 10, 10, 10, 10, 10, 10, 10
    incremento dw 1, 1, 1, 1, 1, 1, 1, 1

section .text
    global _start

_start:
    movdqa xmm0, [variables]
    movdqa xmm1, [incremento]
    paddw xmm0, xmm1 ; xmm0 = xmm0 + xmm1

.parar:
    mov rax, 60
    xor rdi, rdi
    syscall