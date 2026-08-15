section .text:
global _start
_start:
%macro render_celda 0  ; %1 = byte de celda
    mov al, al
    mov ah, al
    
    ; Separar luz (bits 0-3) y sombra (bits 4-7)
    and al, 0x0F          ; luz
    shr ah, 4             ; sombra
    
    ; Si hay sombra predominante, usar caracter de sombra
    cmp ah, al
    jg .use_sombra
    jl .use_luz
    ; iguales -> usar espacio
    
.use_sombra:
    movzx rbx, ah
    cmp rbx, 8
    jle .sombra_ok
    mov rbx, 8
.sombra_ok:
    mov al, [chars_sombra + rbx]
    jmp .print_char
    
.use_luz:
    movzx rbx, al
    cmp rbx, 8
    jle .luz_ok
    mov rbx, 8
.luz_ok:
    mov al, [chars_luz + rbx]
    
.print_char:
    mov [render_buffer + rcx], al
    inc rcx
%endmacro
render_celda
