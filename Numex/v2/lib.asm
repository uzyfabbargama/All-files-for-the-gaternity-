; --- lib.asm actualizado ---
bits 64
default rel
section .data
    global numex_state ; Exportamos el símbolo para Python
    numex_state dq 0, 0, 0, 0, 0, 0, 0, 0 ; 8 quadwords (64 bytes)
    
section .text
global execute_numex

%include "constants.inc"
%include "macros.inc"

execute_numex:
    ; 1. Preservar el entorno (Stack Frame)
    push rbp       ; GUARDAR RBP es obligatorio si lo vas a usar     
    push r12
    push r13
    push r14
    push r15

    ; 2. INICIALIZACIÓN Y CARGA
    lea rbp, [numex_state] ; Usamos LEA para cargar la dirección de memoria 
    %include "start.inc"
    %include "datos.inc" 
    
    ; 3. PROCESAMIENTO
    %include "num.inc"

    ; 4. VOLCADO (¡Antes de los POP!)
    ; Aquí RBP todavía apunta a numex_state
    mov [rbp], rax
    mov [rbp + 8], rbx
    mov [rbp + 16], r10
    mov [rbp + 24], r11
    mov [rbp + 32], r12
    mov [rbp + 40], r13
    mov [rbp + 48], r14
    mov [rbp + 56], r15

    ; 5. LIMPIEZA FINAL
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbp             ; Ahora sí restauramos el ancla
    ret
