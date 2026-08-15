Numex_start:
lea rbp, [rel numex_state] ; Carga la dirección de la memoria en rbp
mov rax, [rbp]
mov rbx, [rbp + 8]
mov r10, [rbp + 16]
mov r11, [rbp + 24]
mov r12, [rbp + 32]
mov r13, [rbp + 40]
mov r14, [rbp + 48]
mov r15, [rbp + 56]
