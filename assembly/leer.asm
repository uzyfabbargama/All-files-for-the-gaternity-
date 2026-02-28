sectinon .data
    msg_prompt db "introduce un byte: ", 0 ;Mensaje para el usuario

section .bss
    byte_leído resb 1                     ;reserva 1 byte para almacenar la entrada

section .text
    global _start

_start:
;Configuración del bucle (rcx = 5), por ejemplo
    mov rcx, 5                            ;iniciializa el contador del bucle rcx a 5. Se ejecutará 5 veces.

bucle_lectura:
    push rcx                              ;guarda el valor de rcx en la pila antes de la llamada al sistema
;1. escribir el prompt (syscall write)
    mov rax, 1                            ;syscall number 1 (write)
    mov rd1, 1                            ;file descriptor 1 (stdout)
    mov rsi, msg_prompt                   ;address of the message
    mov rdx, 20                           ;length of the message ("Introduce un byte")
    syscall                               ;ejecuta la llamada al sistema
;2. leer un byte (syscall read)
    mov rax, 0                            ;syscall number 0 (read)
    mov rdi, 0                            ;file descrptor 0 (stdin)
    mov rsi, byte_leido                   ;addres of the read (just 1 byte)
    syscall                               ;ejecuta la llamada al sisrwma
;Opcional: procesar o mostrar el byte_leido (puedes añadir aquí tu lógica)
;por ejemplo, para mostrar lo que se leyó
    mov rax, 1
    mov rd1, 1
    mov rsi, byte_leido
    mov rdx, 1
    syscall

    pop rcx                               ;recupera el valor de rcx desde la pila
;3. decrementar y comprobar rl bucle
    loop_lectura                          ;decrementa RCX, si el mismo != 0, salta a bucle 'bucle_lectura'

fin_programa:
;Salir del programa (syscall exit)
    mov rax, 60 ;syscall number 60 (exit)
    xor rdi, rdi ;exit code 0
    syscall
