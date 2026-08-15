section .data
    canvas_size equ 256          ; 16 * 16
    pixel_buffer times canvas_size dd 0
section .data
    ; El paquete de configuración inicial para X11
    ; Byte 0: Orden de bytes (0x6C = 'l' para Little Endian, lo que usa tu CPU x86-64)
    ; Byte 2-3: Versión mayor del protocolo (11)
    ; Byte 4-5: Versión menor (0)
    x11_handshake:
        db 0x6c, 0x00          ; 'l' (little-endian) + padding
        dw 11                  ; Protocol-major-version
        dw 0                   ; Protocol-minor-version
        dw 0                   ; Authorization-protocol-name length
        dw 0                   ; Authorization-protocol-data length
        dw 0                   ; Padding
section .text
global _start

_start:
    ; --- PASO 1: INFRAESTRUCTURA (Fuera del bucle) ---
    ; Intentar crear el Socket (X11 usa Stream/TCP o Unix Domain, no UDP normalmente)
    mov rax, 41                 ; sys_socket
    mov rdi, 1                  ; AF_UNIX (X11 local suele usar esto)
    mov rsi, 1                  ; SOCK_STREAM
    mov rdx, 0
    syscall
    
    ; El socket ID queda en RAX. Deberías guardarlo para usarlo después.
    mov r15, rax                ; Guardamos el socket en R15 para no perderlo

    ; --- PASO 2: EL CICLO DE DIBUJO ---
    call _draw_canvas

    ; Aquí iría la syscall 44 (sys_sendto) para enviar el pixel_buffer al socket
    ; ...

    ; Salida limpia para no crashear
    mov rax, 60                 ; sys_exit
    xor rdi, rdi
    syscall

_draw_canvas:
    lea rdi, [pixel_buffer]      ; Apuntar al inicio del canvas
    mov rcx, canvas_size         ; Contador de píxeles (256)
    xor rax, rax

.pixel_loop:
    ; --- LA MAGIA DEL COLOR ---
    mov eax, ecx                 
    shl eax, 8                   
    or  eax, 0xFF0000FF          ; Color dinámico
    
    mov [rdi], eax               ; El MOV sagrado
    
    add rdi, 4                   ; Avanzar 4 bytes (RGBA)
    dec rcx                      ; Decrementar contador manual
    jnz .pixel_loop              ; Saltar si RCX no es cero
    ret
