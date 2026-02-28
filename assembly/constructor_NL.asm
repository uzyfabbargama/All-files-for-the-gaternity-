_start
    mov rax, 0 ;CLASS
    mov rdx, 0 ; contador de líneas
    ;constantes
    ;2 bits del CTRL
    ;3 CTRL tipo con acarreo (1)
    ;1 CTRL tipo sin acarreo (0)
    ;variables
    mov r11, 2 ;bits del slot de un  var umbral 1
    mov r12, 3 ;factor de umbral 1 + su activador
    ;construir
    ;rcx para constantes
    mov rcx, 1 ;rcx = CTRL {0}
    shl rcx, 2 ;rax = 100
    or rax, rcx ;rax = 0100
    shl rax, 2 ; rax = 010000
    mov rcx, 3 ; rcx = CTRL {1}
    shl rcx, 2 ;rcx = 1100
    or rax, rcx; rax = 011100
    shl rax, 2 ; rax = 01110000
    mov rcx, r12 ; rcx = VAR (1)
    shl rcx, r11; rcx = 1100
    or rax, rcx; rax = 01111100
    shr rax, 2; rax = 011111