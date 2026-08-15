; brainfuck.asm - Intérprete Brainfuck Ultra Rápido
; Optimización: Procesa 8 instrucciones a la vez con operaciones de bits
; Celda: 8 bytes (1 dato + 7 para direcciones de salto)

section .data
    font_code db "++++++++++[>+++++++<-]>++.", 0  ; Hola Mundo clásico
    ;font_code db "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.>+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++.", 0
    ;msg_debug: db "X", 10
    ;debug_buffer: db ".", 10
    ;msg_dot: db ".", 10
section .bss
    cell resb 0x1000000  ; 16 MB (para 1M de celdas de 8 bytes)

section .text
global _start

%include "macros.inc"  ; Incluir las macros

_start:
    xor rsi, rsi        ; Puntero a código (font_code)
    xor rbx, rbx        ; Puntero a cinta (cell)
    xor r8, r8          ; Registro temporal para patrones
    xor r9, r9          ; Registro temporal
    xor r10, r10        ; Registro temporal
    ;debug_print_rsi
    ; ============================================
    ; PASO 1: PREPROCESADO DE BUCLES
    ; ============================================
    jmp loopProcess

loopProcess:
	;debug_print_rsi
	xor rbx, rbx        ; <--- Asegurar que rbx = 0
    crear_loop          ; Encuentra '[' y ']', guarda saltos en la cinta
    inc rsi
    cmp byte [font_code+rsi], 0
    jnz loopProcess
    
    ; ============================================
    ; PASO 2: EJECUCIÓN
    ; ============================================
    xor rsi, rsi        ; Reiniciar puntero a código
    jmp running

running:
    ;debug_running
    ;debug_print_rsi
    ; Detectar y ejecutar patrones (8 bytes a la vez)
    xor r10, r10
    detectar_plus
    xor r10, r10
    detectar_minus
    xor r10, r10
    detectar_left
    xor r10, r10
    detectar_right
    xor r10, r10
    output_char         ; Implementado
    xor r10, r10
    input_char          ; Implementado
    xor r10, r10
    ; Manejo de bucles (O(1) con tabla de saltos)
    access_bucle_start
    xor r10, r10
    access_bucle_end
    xor r10, r10
    
    inc rsi
    cmp byte [font_code+rsi], 0
    jnz running
	jmp exit
exit:
    mov rax, 60
    xor rdi, rdi
    syscall
