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

; Cámara (Posición en el mapa de 1MB)
cam_x     dq 0
cam_y     dq 0

; Estructura para nanosleep (16ms = ~60fps)
timespec:
    dq 0, 16666666

section .text
global _start

_start:
    ; 1. CARGAR UNIVERSO
    mov rax, 2                  ; open
    mov rdi, filename
    mov rsi, 0                  ; O_RDONLY
    syscall
    test rax, rax
    js .error_exit              
    
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
    js .error_exit              
    mov r8, rax                 ; Guardar fd

    ; mmap para proyectar el video en la RAM
    mov rax, 9                  ; syscall mmap
    xor rdi, rdi
    mov rsi, screen_size
    mov rdx, 3                  ; PROT_READ | PROT_WRITE
    mov r10, 1                  ; MAP_SHARED
    xor r9, r9
    syscall
    mov [fb_ptr], rax           ; Guardamos el puntero de video

.main_loop:
    call _render_view
    
    ; Pausa para sincronía y que el Athlon no sufra
    mov rax, 35                 ; nanosleep
    mov rdi, timespec
    xor rsi, rsi
    syscall
    
    jmp .main_loop

.error_exit:
    mov rax, 60                 ; sys_exit
    mov rdi, 1                  ; Error
    syscall

_render_view:
    mov r12, [fb_ptr]           ; R12 = inicio de la pantalla
    mov r14, 0                  ; Contador de filas de bloques

.row_loop:
    push r14
    mov r15, 0                  ; Contador de columnas de bloques

.col_loop:
    ; Calcular índice: (cam_y + r14) * 1000 + (cam_x + r15)
    mov rax, [cam_y]
    add rax, r14
    imul rax, 1000
    add rax, [cam_x]
    add rax, r15
    
    ; Seguridad de límites
    cmp rax, 1000000
    jae .out_of_bounds

    movzx ebx, byte [universo + rax] 
    
    ; Generar color ARGB basado en el byte del universo
    mov eax, ebx
    shl eax, 16                 ; R
    mov al, bl                  ; B
    shl ebx, 8
    or  eax, ebx                ; G
    or  eax, 0xFF000000         ; Alpha
    jmp .draw

.out_of_bounds:
    mov eax, 0xFF000000         ; Negro

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
    ; Pinta el bloque en la pantalla usando rep stosd
    push rdi
    push r14
    push r15
    push rax

    ; Calcular posición en pantalla
    mov rdi, r14
    imul rdi, chunk_p
    imul rdi, screen_w
    mov rbx, r15
    imul rbx, chunk_p
    add rdi, rbx
    shl rdi, 2
    add rdi, r12                ; Destino final en RDI

    mov rdx, chunk_p            ; Alto
.chunk_h_loop:
    push rdx
    push rdi
    mov rcx, chunk_p            ; Ancho
    rep stosd                   ; ¡Velocidad Transurgente!
    pop rdi
    add rdi, screen_w * 4       ; Bajar una línea de píxeles
    pop rdx
    dec rdx
    jnz .chunk_h_loop

    pop rax
    pop r15
    pop r14
    pop rdi
    ret
