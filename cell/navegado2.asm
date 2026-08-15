; -----------------------------------------------------------------------
; NAVEGADOR TRANSURGENTE - MÓDULO DE EXPLORACIÓN (x86-64 NASM)
; -----------------------------------------------------------------------
; Controles: WASD para moverse, Q para salir.
; -----------------------------------------------------------------------

section .bss
universo: resb 1000000
fb_ptr:   resq 1
input_buf: resb 1

section .data
fb_path   db "/dev/fb0", 0
filename  db "universo.bin", 0
screen_w  equ 1920
screen_h  equ 1080
screen_size equ screen_w * screen_h * 4
chunk_p   equ 32
view_w    equ 40
view_h    equ 30

cam_x     dq 0
cam_y     dq 0

timespec: dq 0, 16666666 ; 60 FPS

section .text
global _start

_start:
; 1. CARGAR UNIVERSO
mov rax, 2
mov rdi, filename
mov rsi, 0
syscall
test rax, rax
js .error_exit
mov rdi, rax
mov rax, 0
mov rsi, universo
mov rdx, 1000000
syscall
mov rax, 3
syscall

; 2. FRAMEBUFFER SETUP
mov rax, 2
mov rdi, fb_path
mov rsi, 2
syscall
mov r8, rax
mov rax, 9
xor rdi, rdi
mov rsi, screen_size
mov rdx, 3
mov r10, 1
xor r9, r9
syscall
mov [fb_ptr], rax



.main_loop:
call _render_view
call _check_input     ; <--- NUEVA FUNCIÓN DE MOVIMIENTO

; Pausa
mov rax, 35
mov rdi, timespec
xor rsi, rsi
syscall
jmp .main_loop

.error_exit:
mov rax, 60
mov rdi, 1
syscall
_check_input:
; Leer teclado de forma no bloqueante (stdin)
; Nota: Esto funciona mejor si usas 'stty -icanon -echo' antes de correrlo
mov rax, 0          ; sys_read
mov rdi, 0          ; stdin
mov rsi, input_buf
mov rdx, 1
; Hacemos el read no bloqueante usando flags de sistema o simplemente
; aceptando que en TTY pura a veces espera.
; Para simplicidad extrema, usaremos una syscall de sondeo:

; --- Check para WASD ---
mov al, [input_buf]
cmp al, 'w'
je .up
cmp al, 's'
je .down
cmp al, 'a'
je .left
cmp al, 'd'
je .right
cmp al, 'q'
je .exit
ret


.up:
cmp qword [cam_y], 0
jle .done
sub qword [cam_y], 1
jmp .done
.down:
cmp qword [cam_y], 1000 - view_h
jge .done
add qword [cam_y], 1
jmp .done
.left:
cmp qword [cam_x], 0
jle .done
sub qword [cam_x], 1
jmp .done
.right:
cmp qword [cam_x], 1000 - view_w
jge .done
add qword [cam_x], 1
jmp .done
.exit:
mov rax, 60
xor rdi, rdi
syscall
.done:
mov byte [input_buf], 0 ; Limpiar buffer
ret

_render_view:
mov r12, [fb_ptr]
mov r14, 0
.row_loop:
push r14
mov r15, 0
.col_loop:
mov rax, [cam_y]
add rax, r14
imul rax, 1000
add rax, [cam_x]
add rax, r15

cmp rax, 1000000
jae .out_of_bounds
movzx ebx, byte [universo + rax] 

; Color: Usamos el byte para crear un tinte
mov eax, ebx
shl eax, 16
mov al, bl
shl ebx, 8
or  eax, ebx
or  eax, 0xFF000000
jmp .draw


.out_of_bounds:
mov eax, 0xFF000000
.draw:
call _draw_chunk
inc r15
cmp r15, view_w
jl .col_loop
pop r14
inc r14
cmp r14, view_h
jl .row_loop
ret

_draw_chunk:
push rdi
push r14
push r15
push rax
mov rdi, r14
imul rdi, chunk_p
imul rdi, screen_w
mov rbx, r15
imul rbx, chunk_p
add rdi, rbx
shl rdi, 2
add rdi, r12
mov rdx, chunk_p
.chunk_h_loop:
push rdx
push rdi
mov rcx, chunk_p
rep stosd
pop rdi
add rdi, screen_w * 4
pop rdx
dec rdx
jnz .chunk_h_loop
pop rax
pop r15
pop r14
pop rdi
ret

