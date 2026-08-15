Numex_start:
lea rbp, [rel numex_state] ; Carga la dirección de la memoria en rbp
mov rax, max
mov rbx, max
mov r10, max
mov r11, max
mov r12, max
mov r13, max
mov r14, max
mov r15, max ;bueno, son 9 registros, en la práctica son 567 bits (64×9 - 9)
jmp _todo
