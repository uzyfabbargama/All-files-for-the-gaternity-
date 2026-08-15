section .data
    fb_path db "/dev/fb0", 0
    screen_size equ 1920 * 1080 * 4 ; Ajusta a tu resolución (Ancho * Alto * 4)

section .text
global _start

_start:
    ; 1. Abrir el Framebuffer
    mov rax, 2          ; sys_open
    mov rdi, fb_path    ; Ruta al dispositivo
    mov rsi, 2          ; O_RDWR (Lectura y Escritura)
    syscall
    
    ; El File Descriptor queda en RAX. Lo guardamos en R15.
    mov r15, rax

    ; 2. mmap (Mapear la pantalla a RAM)
    ; Queremos que el kernel nos dé una dirección de memoria
    mov rax, 9          ; sys_mmap
    xor rdi, rdi        ; Que el kernel elija la dirección
    mov rsi, screen_size ; Tamaño de la pantalla en bytes
    mov rdx, 3          ; PROT_READ | PROT_WRITE
    mov r10, 1          ; MAP_SHARED (Para que los cambios se vean)
    mov r8, r15         ; El file descriptor de /dev/fb0
    xor r9, r9          ; Offset 0
    syscall

    ; ¡AHORA RAX TIENE LA DIRECCIÓN DE MEMORIA DE TU PANTALLA!
    mov rdi, rax        ; RDI apunta al primer píxel (arriba a la izquierda)

    ; 3. El Bucle de Dibujado (Tu especialidad)
    mov rcx, 1024       ; Vamos a pintar una línea o un bloque
.draw_loop:
    mov dword [rdi], 0x00FF0000 ; ¡PUM! Píxel Rojo (BGRA o RGBA)
    add rdi, 4          ; Siguiente píxel
   ; En lugar de r8 y cmp...
    mov ecx, 10000              ; Cantidad de píxeles
    mov eax, 0x00FF0000         ; Color Rojo
    rep stosd                   ; ¡MAGIA! Repite "store string" (EAX -> [RDI]) 
                                ; y avanza RDI automáticamente 10,000 veces.

    ; 4. Salir (En la vida real, querrías un bucle infinito aquí para ver el dibujo)
    mov rax, 60
    xor rdi, rdi
    syscall
