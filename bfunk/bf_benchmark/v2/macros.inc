; macros.inc - Todas las macros del intérprete
%include "rsi_control.inc"
%include "Cell_control.inc"
%include "patterns_detector.inc"
%include "loops_control.inc"
%include "IO_control.inc"



; ============================================
; DEBUG DE RESGISTROS
; ============================================
%macro debug_print_rsi 0
;    push rax
;    push rdi
;    push rsi
;    push rdx
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, debug_buffer
;    mov rdx, 1
;    syscall
;    pop rdx
;    pop rsi
;    pop rdi
;    pop rax
nop
%endmacro
%macro debug_running 0
; Debug: imprimir un carácter para saber que llegamos
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, msg_debug
;    mov rdx, 1
;    syscall
nop
%endmacro

%macro debug_output 0
;	; Debug: imprimir un carácter
;    mov rax, 1
;    mov rdi, 1
;    mov rsi, msg_dot
;    mov rdx, 1
;    syscall
nop
%endmacro
