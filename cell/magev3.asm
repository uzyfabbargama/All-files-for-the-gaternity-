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
    ; 1. CARGAR UNIVERSO
    mov rax, 2                  ; open
    mov rdi, filename
    mov rsi, 0                  ; O_RDONLY
    syscall
    test rax, rax
    js .error_exit              ; Salto local a _start.error_exit
    
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
    test rax, rax
    js .error_exit              ; Salto local a _start.error_exit
    mov r8, rax                 ; fd del fb

    mov rax, 9                  ; mmap
    xor rdi, rdi
    mov rsi, screen_size
    mov rdx, 3                  ; PROT_READ | PROT_WRITE
    mov r10, 1                  ; MAP_SHARED
    xor r9, r9
    syscall
    mov [fb_ptr], rax           ; Guardamos el inicio de la pantalla

.main_loop:
    call _render_view
    
    ; Pausa para sincronía
    mov rax, 35                 ; nanosleep
    mov rdi, .timespec
    xor rsi, rsi
    syscall
    
    jmp .main_loop
section .data
.timespec:
    dq 0, 16666666              ; ~60 FPS

.error_exit:
    ; Esta es la salida de emergencia de _start
    mov rax, 60                 ; sys_exit
    mov rdi, 1                  ; Código de error 1
    syscall

_render_view:
    mov r12, [fb_ptr]           ; R12 = base de pantalla
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
    
    ; Evitar salirnos del 1MB si cam_x/y son muy grandes
    cmp rax, 1000000
    jae .out_of_bounds

    movzx ebx, byte [universo + rax] ; Obtener el byte (bioma)
    
    ; Lógica de color transurgente
    mov eax, ebx
    shl eax, 16                 ; Canal Rojo
    mov al, bl                  ; Canal Azul
    shl ebx, 8
    or  eax, ebx                ; Canal Verde
    or  eax, 0xFF000000         ; Alpha al máximo (Opaco)
    jmp .draw

.out_of_bounds:
    mov eax, 0xFF000000         ; Negro si estamos fuera del mapa

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
    ; Pinta un cuadrado sólido de color EAX
    push rdi
    push r14
    push r15
    push rax

    ; offset = (r14*chunk_p*screen_w + r15*chunk_p)*4
    mov rdi, r14
    imul rdi, chunk_p
    imul rdi, screen_w
    mov rbx, r15
    imul rbx, chunk_p
    add rdi, rbx
    shl rdi, 2
    add rdi, r12                ; RDI tiene la dirección física en video

    mov rcx, chunk_p            ; Alto del bloque
.chunk_h:
    push rcx
    push rdi
    mov rcx, chunk_p            ; Ancho del bloque
    rep stosd                   ; Transferencia ultra-rápida de color
    pop rdi
    add rdi, screen_w * 4       ; Siguiente línea de píxeles
    pop rcx
    loop .chunk_h

    pop rax
    pop r15
    pop r14
    pop rdi
    ret

