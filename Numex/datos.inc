; rdi (tipo) 
; rsi 1er
; rdx 2do
; rcx 3er
; r8  4t0
_Datos:
test rdi, rdi
jnz .bottom
jz .top
.bottom:
add rax, rsi
add rbx, rdx
add r10, rcx
add r11, r8
.top:
add r12, rsi
add r13, rdx
add r14, rcx
add r15, r8
