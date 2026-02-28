;rcx (componentes), rdx(offser acumulativo)
_start
    mov rax, 0 ;registro CLASS
    mov rdx, 0 ;acumulador de bits
    ;constantes
    ;2 bits de CTRL
    ; 3 = CTRL {1}
    ; 1 = CTRL {0}
    mov r8, 3 ;umbral + bit de activación
    mov r9, 2 ;cantidad de bits
    mov rcx, r8 ;rcx = VAR (1), línea 0
    or rax, rcx ; rax = 11
    sub r9, 1 ; r9 = 1
    shl rdx, r9 ; rdx = desplazamiento flexible por N bits
    add r9, 1 ; r9 = 2
    mov rcx, 3 ; rcx = CTRL {1}
    shl rcx, rdx ;rcx = 1100
    or rax, rcx ;rax = 1111
    shl rdx, 1 ;rdx = 4
    mov rcx, 1 ; rcx = CTRL {0}
    shl rcx, rdx ;rcx = 010000
    or rax, rcx ; rax = 011111
    ;#esto es igual a
    ;CLASS clase = VAR variable(1),
    ;CTRL {1},
    ;CTRL {0});
    ;uso
    ;0[1] 1[1] [1]1 (bits objetivos, los CTRL tienen el bit atrás, y las VAR adelante)
    mov r8, 1 ;para var
    mov r9, 2 ;para CTRL {0}
    mov r10, 4 ;para CTRL {1}
    mov r11, 1;bit de activación (constante) 1 r11
    mov rbx, 0 ;para almacenar la class espejo
    shl r11, r8 ;r11 = 2
    or rbx, r11 ;rbx = 2
    mov r11, 1 ;reestablecer
    shl r11, r9 ;r11 = 4 (100)
    or rbx, r11 ;rbx = 1010
    mov r11, 1 ; r11 = 1
    shl r11, r10; r11 = 10000
    or rbx, r11 ;rbx = 10110
    mov rex, rbx
    xor rex, rax ;si hay iguales se anulan, 