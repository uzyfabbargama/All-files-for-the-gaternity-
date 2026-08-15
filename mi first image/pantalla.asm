section .data
    display_name db 0          ; Usar el DISPLAY por defecto (:0)
    title        db "Consola Ladrillo Gris - Negro Absoluto", 0

section .bss
    display      resq 1        ; Puntero al Display de X11
    window       resq 1        ; ID de la ventana
    visual       resq 1        ; Estructura Visual
    gc           resq 1        ; Contexto Gráfico (Graphics Context)

section .text
    global _start

; --- Declaración de funciones externas de X11 ---
extern XOpenDisplay
extern XCreateSimpleWindow
extern XSelectInput
extern XMapWindow
extern XCreateGC
extern XSetForeground
extern XFillRectangle
extern XFlush
extern XCloseDisplay

_start:
    ; 1. Abrir la conexión con el servidor gráfico X11
    mov rdi, display_name
    call XOpenDisplay
    test rax, rax
    jz exit_error              ; Si devuelve 0, error
    mov [display], rax

    ; Obtener variables necesarias del display (DefaultScreen, RootWindow)
    ; Para mantenerlo minimalista, usamos valores por defecto directos
    mov rdi, [display]         ; display
    mov rsi, qword [rax + 24]  ; RootWindow (offset típico en estructura)
    mov rdx, 10                ; Posición X
    mov r10, 10                ; Posición Y
    mov r8, 512                ; Ancho (¡Potencia de 2 para tus desplazamientos!)
    mov r9, 512                ; Alto
    push 0x000000              ; Color de fondo: Negro Absoluto (#000000)
    push 0x000000              ; Color de borde
    push 1                     ; Ancho de borde
    call XCreateSimpleWindow
    add rsp, 24                ; Limpiar el stack de los 3 pushes
    mov [window], rax

    ; 2. Crear el Contexto Gráfico (GC) para poder pintar píxeles
    mov rdi, [display]
    mov rsi, [window]
    mov rdx, 0
    mov r10, 0
    call XCreateGC
    mov [gc], rax

    ; 3. Mapear (mostrar) la ventana en pantalla
    mov rdi, [display]
    mov rsi, [window]
    call XMapWindow

    ; 4. Pintar la pantalla de negro usando el GC
    mov rdi, [display]
    mov rsi, [window]
    mov rdx, [gc]
    mov rcx, 0x000000          ; Color Negro de nuevo
    call XSetForeground

    ; Dibujar el rectángulo que ocupa toda la pantalla (512x512)
    mov rdi, [display]
    mov rsi, [window]
    mov rdx, [gc]
    mov rcx, 0                 ; X
    mov r8, 0                  ; Y
    mov r9, 512                ; Ancho
    push 512                   ; Alto (se pasa por stack o registro según convención extendida)
    mov r9, 512
    ; En sistemas limpios, XFillRectangle dibuja directo en el buffer
    call XFillRectangle
    pop r9

    ; Enviar comandos al servidor gráfico para que impacte el cambio
    mov rdi, [display]
    call XFlush

; --- Bucle infinito minimalista para mantener la pantalla abierta ---
bucle_espera:
    ; Acá en el futuro irá tu parser de HTML y chunks.
    ; Por ahora, se queda esperando para que no se cierre.
    jmp bucle_espera

exit_error:
    ; Salida limpia por Syscall (sys_exit = 60)
    mov rax, 60
    mov rdi, 1                 ; Código de error 1
    syscall
