; --- PANTALLA NEGRA ROBUSTA (X11 x86-64) ---
; Solución al Segfault: Alineación de Stack y paso de argumentos corregido.

section .data
    display_name db 0          ; Usar DISPLAY por defecto
    
section .bss
    display      resq 1        ; Guardar puntero al Display
    window       resq 1        ; Guardar ID de Ventana
    gc           resq 1        ; Guardar Contexto Gráfico
    root_win     resq 1        ; Guardar Root Window ID
    screen_num   resd 1        ; Número de pantalla (dword)

section .text
    global _start

; Definiciones de funciones externas de libX11
extern XOpenDisplay
extern XRootWindow
extern XDefaultScreen
extern XCreateSimpleWindow
extern XMapWindow
extern XCreateGC
extern XSetForeground
extern XFillRectangle
extern XFlush
extern XSync

_start:
    ; --- 1. ALINEAR EL STACK A 16 BYTES (CRÍTICO PARA LLAMADAS C) ---
    ; Guardamos el rsp original en rbp para restaurarlo al final (opcional en _start)
    mov rbp, rsp
    and rsp, -16               ; Asegurar alineación de 16 bytes

    ; --- 2. ABRIR CONEXIÓN X11 ---
    mov rdi, display_name      ; Arg 1: Nombre del display (NULL)
    call XOpenDisplay
    test rax, rax
    jz exit_error              ; Si falla, salir
    mov [display], rax         ; Guardar puntero

    ; --- 3. OBTENER DATOS DE PANTALLA POR DEFECTO ---
    mov rdi, [display]
    call XDefaultScreen
    mov [screen_num], eax       ; Guardar número de pantalla (eax es 32-bit int)

    mov rdi, [display]
    mov rsi, rax               ; Usar el número de pantalla recién obtenido
    call XRootWindow
    mov [root_win], rax        ; Guardar Root Window

    ; --- 4. CREAR LA VENTANA (CORREGIDO PASO DE ARGUMENTOS) ---
    ; XCreateSimpleWindow(display, parent, x, y, width, height, border_width, border, background)
    ; Argumentos en registros: RDI, RSI, RDX, RCX, R8, R9
    ; Argumentos en Stack: 7º, 8º, 9º...

    ; Preparar argumentos del Stack primero (en orden inverso)
    push 0x000000              ; Arg 9: Color de fondo (Negro)
    push 0x000000              ; Arg 8: Color del borde
    push 1                     ; Arg 7: Ancho del borde

    ; Preparar argumentos en registros
    mov rdi, [display]         ; Arg 1
    mov rsi, [root_win]        ; Arg 2
    mov rdx, 100               ; Arg 3: Posición X
    mov rcx, 100               ; Arg 4: Posición Y
    mov r8, 512                ; Arg 5: Ancho
    mov r9, 512                ; Arg 6: Alto

    call XCreateSimpleWindow
    add rsp, 24                ; LIMPIAR STACK (3 * 8 bytes)
    test rax, rax
    jz exit_error
    mov [window], rax          ; Guardar ID de ventana

    ; --- 5. CREAR CONTEXTO GRÁFICO (GC) ---
    mov rdi, [display]
    mov rsi, [window]
    mov rdx, 0                 ; valuemask
    mov rcx, 0                 ; values
    call XCreateGC
    test rax, rax
    jz exit_error
    mov [gc], rax

    ; --- 6. MOSTRAR LA VENTANA ---
    mov rdi, [display]
    mov rsi, [window]
    call XMapWindow

    ; --- 7. PINTAR EL LIENZO DE NEGRO (CORREGIDO) ---
    ; Establecer color de dibujo en negro
    mov rdi, [display]
    mov rsi, [gc]              ; Corregido: XSetForeground usa el GC, no la ventana
    mov rdx, 0x000000          ; Color Negro
    call XSetForeground

    ; Dibujar rectángulo negro (XFillRectangle usa el mismo orden de args en stack)
    push 512                   ; Arg 7: Alto
    mov rdi, [display]         ; Arg 1
    mov rsi, [window]          ; Arg 2
    mov rdx, [gc]              ; Arg 3
    mov rcx, 0                 ; Arg 4: X
    mov r8, 0                  ; Arg 5: Y
    mov r9, 512                ; Arg 6: Ancho
    call XFillRectangle
    add rsp, 8                 ; Limpiar stack del alto

    ; --- 8. SINCRONIZAR Y FORZAR DIBUJO ---
    mov rdi, [display]
    mov rsi, 0                 ; discard (false)
    call XSync                 ; Más robusto que XFlush para asegurar el primer dibujado

; --- BUCLE INFINITO (LIENZO VACÍO) ---
bucle_espera:
    jmp bucle_espera

exit_error:
    mov rsp, rbp               ; Restaurar stack original (buena práctica)
    mov rax, 60                ; sys_exit
    mov rdi, 1                 ; Código de error
    syscall
