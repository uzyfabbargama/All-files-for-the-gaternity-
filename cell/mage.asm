; -----------------------------------------------------------------------
; NAVEGADOR TRANSURGENTE DEL UNIVERSO (x86-64 NASM)
; -----------------------------------------------------------------------
; Instrucciones:
; 1. Compilar con: nasm -f elf64 navegador.asm -o navegador.o
; 2. Linkear con:  ld navegador.o -o navegador
; 3. Ejecutar:     sudo ./navegador (Requiere acceso a /dev/fb0)
; -----------------------------------------------------------------------

section .bss
universo: resb 1000000      ; Tu 1 MB de datos
fb_ptr:   resq 1            ; Puntero al framebuffer mapeado

section .data
fb_path   db "/dev/fb0", 0
filename  db "universo.bin", 0

; Configuración de pantalla (Ajustar a tu resolución de Lubuntu)
screen_w  equ 1920
screen_h  equ 1080
screen_size equ screen_w * screen_h * 4

; Configuración de visualización
chunk_p   equ 32            ; Tamaño del bloque (píxeles)
view_w    equ 40            ; Cuántos bloques de ancho mostrar
view_h    equ 30            ; Cuántos bloques de alto mostrar

; Cámara
cam_x     dq 0
cam_y     dq 0


section .text
global _start

_start:
; 1. CARGAR UNIVERSO (Tu código original simplificado)
mov rax, 2                  ; open
mov rdi, filename
mov rsi, 0                  ; O_RDONLY
syscall
test rax, rax
js .error_exit              ; Si no hay archivo, fuera

mov rdi, rax
mov rax, 0                  ; read
mov rsi, universo
mov rdx, 1000000
syscall

mov rax, 3                  ; close
syscall

; 2. PREPARAR FRAMEBUFFER
mov rax, 2                  ; open
mov rdi, fb_path
mov rsi, 2                  ; O_RDWR
syscall
mov r8, rax                 ; fd del fb

mov rax, 9                  ; mmap
xor rdi, rdi
mov rsi, screen_size
mov rdx, 3                  ; PROT_READ | PROT_WRITE
mov r10, 1                  ; MAP_SHARED
xor r9, r9
syscall
mov [fb_ptr], rax           ; Guardamos el inicio de la pantalla

.error_exit:
mov rax, 60
mov rdi, 1
syscall
section .data
.timespec:
dq 0, 16666666          ; ~60 FPS (16ms)

.main_loop:
call _render_view

; Aquí podríamos añadir la lectura de teclado para mover cam_x/cam_y
; Por ahora, una pausa para que el Athlon respire
mov rax, 35                 ; nanosleep
mov rdi, .timespec
xor rsi, rsi
syscall

jmp .main_loop


_render_view:
; rdi = destino en pantalla
; rsi = origen en universo
mov r12, [fb_ptr]           ; R12 = base de pantalla
mov r13, [cam_y]            ; Fila actual del universo

mov r14, 0                  ; Contador de filas de bloques (view_h)


.row_loop:
push r14
mov r15, 0                  ; Contador de columnas de bloques (view_w)

.col_loop:
; Calcular índice en el universo: (cam_y + r14) * 1000 + (cam_x + r15)
mov rax, [cam_y]
add rax, r14
imul rax, 1000
add rax, [cam_x]
add rax, r15

movzx ebx, byte [universo + rax] ; Obtener el byte (bioma)

; Convertir byte a color (usando tu lógica de color)
; Ejemplo: byte * algo para crear un color ARGB
mov eax, ebx
shl eax, 16                 ; R
mov al, bl                  ; B
shl ebx, 8
or  eax, ebx                ; G
or  eax, 0xFF000000         ; Alpha Full

; Dibujar el cuadrado de 32x32 píxeles
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
; Esta subrutina pinta un bloque de chunk_p x chunk_p en la posición actual
; Usa EAX como color, R12 como base de pantalla, r14/r15 para coords
push rdi
push r14
push r15

; Calcular offset inicial en pantalla
; offset = (r14 * chunk_p * screen_w + r15 * chunk_p) * 4
mov rdi, r14
imul rdi, chunk_p
imul rdi, screen_w
mov rbx, r15
imul rbx, chunk_p
add rdi, rbx
shl rdi, 2                  ; *4 bytes
add rdi, r12                ; Añadir base mmap

mov rcx, chunk_p            ; Alto del bloque


.chunk_h:
push rcx
push rdi
mov rcx, chunk_p            ; Ancho del bloque
rep stosd                   ; ¡REP STOSD! Velocidad pura
pop rdi
add rdi, screen_w * 4       ; Siguiente línea de pantalla
pop rcx
loop .chunk_h

pop r15
pop r14
pop rdi
ret



