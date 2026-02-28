
section .data

;Ensamblador: NASM (netwide assembler)
; arquitectura: x86-64 (amd64)

section .data
    ;buffer para guardar el resultado de la conversión (ASCII)
    resultado db "00", 0Ah ; "00" + salto de línea (0Ah)

section .text 
    global _start

_start:
; ---- PARTE 1: cálculo (42 + 10 = 52) ----
    mov rax, 42
    mov rbx, 10
    add rax, rbx

; ---- PARTE 2: conversión a ASCII ----
; Para imprimir el número 52, debemos convertirlo a los caracteres "5" y "2"

;1. Convertir el dígito de las unidades (2)

    mov rdi, rax ;copia el resultado (52) para manipularlo
    mov rcx, 10 ;divisor para obtener el digito
    mov rdx, 0 ; Limpia rdx para la divsión de 64 bits (RDX:RAX / RCX)
    div rcx ; RAX = 5 (cociente), rDX = 2 (resto)
    add dl, '0' ;convierte el resto (2) a su caracter ASCII ('2')
    MOV [resultado + 1], dl ; Almacena el carácter '2' en el segundo byte del buffer
    ;2. convertir el digito de las decenas (5)
    mov rdx, 0 ;Limpia RDX para la siguiente división}
    mov rcx, 10 ;Divisor (10)
    div rcx ; Ahora rax = 5 (cociente), rdx = 0 (resto)
    add dl, '0' ;Convierte el resto (5) a su valor ascii ('5')
    mov [resultado], DL ;almacena el carácter en el buffer
    ; ---- PARTE 3: LLAMADA AL SISTEMA PARA IMPRIMIR (SYSCALL write) ----
    ;Linux syscall: write (syscall #1)
    mov rax, 1 ;códcigo de syscall para 'write' (escribir)
    ; Agumentos para la syscall 'write' (escribir)
    mov rdi, 1 ; Argumento 1: Descritor de archivo (1 = stdout - salida estándar)
    mov rsi, resultado;Argumento 2: Dirección del buffer (nuestro '52' convertido)
    mov rdx, 3 ; argumento 3: Número de bytes a escribir (los dos dígitos '5', '2' + salto de línea oAh)
    SYSCALL ;ejecuta la llamada al sistema

    ;----PARTE 4: LLAMADA AL SISTEMA PARA SALIR (SYSCALL exit) ----
    
    ;Linux syscall: exit
    mov rax, 60 ;código de syscall para 'exit' (salir)
    ;Argumentos para la syscall 'exit':
    mov rdi, 0 ; argumento 1: código de retorno (0 = éxito)
    SYSCALL ; ejecuta la llamada al sistema