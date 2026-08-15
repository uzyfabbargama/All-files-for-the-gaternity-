; ============================================================
; visual.asm - Motor de Renderizado para universo.asm
; Incluir con: %include "visual.asm"
; Uso: llamar a render_criaturas después de cada update
; ============================================================

section .data
    ; Mapa de caracteres ASCII según densidad de bits
    chars_sombra db " .:oO0@#", 0
    chars_luz    db ' "`^\"*+xX%', 0   ; comilla simple afuera, doble adentro
    
    ; Colores ANSI (si terminal lo soporta)
    color_normal   db 27, "[0m", 0
    color_sombra   db 27, "[30;47m", 0  ; gris oscuro sobre blanco
    color_luz      db 27, "[37;40m", 0  ; blanco sobre negro
    color_ojo      db 27, "[31;43m", 0  ; rojo sobre amarillo (¡ojos negros!)
    
    ; Configuración de cámara
    cam_x dq 500    ; centro X (universo de 1000x1000)
    cam_y dq 500    ; centro Y
    zoom   dq 2     ; celdas por píxel
    
    ; Detección de criaturas
    threshold_criatura dq 30  ; mínimo de "energía" para considerar criatura
    
section .bss
    ; Buffer de renderizado (80x24 = 1920 bytes aprox)
    render_buffer: resb 2000
    ; Lista de coordenadas de criaturas detectadas
    criaturas_x: resq 100
    criaturas_y: resq 100
    criaturas_energia: resq 100
    num_criaturas: resq 1

section .text

; ------------------------------------------------------------
; Macro: detectar_criaturas
; Escanea el universo y encuentra patrones con alta densidad
; ------------------------------------------------------------
%macro detectar_criaturas 0
    push rsi
    push rcx
    push rax
    push rbx
    
    mov qword [num_criaturas], 0
    mov rsi, universo
    add rsi, 2000          ; inicio del universo útil
    mov rcx, 996000        ; total de celdas
    xor rbx, rbx           ; contador de criaturas
    
.scan_loop:
    ; Leer celda actual
    movzx rdx, byte [rsi]
    
    ; Saltar si es muy baja energía (bits 0-7 sumados)
    mov al, dl
    and al, 0xFF
    cmp al, [threshold_criatura]
    jb .next_cell
    
    ; Calcular coordenadas (aproximadas)
    mov rax, rsi
    sub rax, universo
    sub rax, 2000
    mov r8, 1000
    xor rdx, rdx
    div r8                 ; rax = Y, rdx = X
    
    ; Guardar criatura
    mov r9, [num_criaturas]
    cmp r9, 99
    je .next_cell
    
    mov [criaturas_x + r9*8], rdx
    mov [criaturas_y + r9*8], rax
    movzx r10, byte [rsi]
    mov [criaturas_energia + r9*8], r10
    
    inc qword [num_criaturas]
    
.next_cell:
    inc rsi
    loop .scan_loop
    
    pop rbx
    pop rax
    pop rcx
    pop rsi
%endmacro

; ------------------------------------------------------------
; Macro: render_celda
; Renderiza una celda según su contenido (luz vs sombra)
; ------------------------------------------------------------
%macro render_celda 1  ; %1 = byte de celda
    mov al, %1
    mov ah, al
    
    ; Separar luz (bits 0-3) y sombra (bits 4-7)
    and al, 0x0F          ; luz
    shr ah, 4             ; sombra
    
    ; Si hay sombra predominante, usar caracter de sombra
    cmp ah, al
    jg .use_sombra
    jl .use_luz
    ; iguales -> usar espacio
    
.use_sombra:
    ; En lugar de movzx rbx, ah
    mov al, ah          ; Movemos el valor de AH a AL
    movzx rbx, al       ; Ahora sí, de AL a RBX es seguro
    cmp rbx, 8
    jle .sombra_ok
    mov rbx, 8
.sombra_ok:
    mov al, [chars_sombra + rbx]
    jmp .print_char
    
.use_luz:
    movzx rbx, al
    cmp rbx, 8
    jle .luz_ok
    mov rbx, 8
.luz_ok:
    mov al, [chars_luz + rbx]
    
.print_char:
    mov [render_buffer + rcx], al
    inc rcx
%endmacro

; ------------------------------------------------------------
; Macro: renderizar_pantalla
; Renderiza la región actual del universo usando ASCII
; ------------------------------------------------------------
renderizar_pantalla:
    push rsi
    push rcx
    push rax
    push rbx
    
    ; Limpiar render_buffer con espacios (32 en ASCII)
    mov rcx, 2000
    mov rdi, render_buffer
    mov al, 32
    rep stosb
    
    ; Coordenadas de la cámara
    mov r8, [cam_x]
    mov r9, [cam_y]
    mov r10, [zoom]
    
    ; Calcular inicio del scan en universo
    mov rsi, universo
    add rsi, 2000
    mov rax, r9
    sub rax, 12          ; media pantalla en Y (asumiendo 24 filas)
    imul rax, 1000
    add rsi, rax
    mov rax, r8
    sub rax, 40          ; media pantalla en X (asumiendo 80 cols)
    add rsi, rax
    
    ; Renderizar fila por fila
    mov rbx, 0           ; fila
    mov rcx, 0           ; columna
    
.row_loop:
    cmp rbx, 24
    jge .row_done
    
.col_loop:
    cmp rcx, 80
    jge .col_done
    
    ; Obtener celda (con zoom)
    ; Protección contra rsi loco
    cmp rsi, universo
    jb .pintar_espacio
    cmp rsi, universo + 1000000
    jae .pintar_espacio
    
    movzx rax, byte [rsi + rcx]
    jmp .continuar
    
.pintar_espacio:
    mov al, ' '
.continuar:
    render_celda al
    
    add rcx, 1
    jmp .col_loop
    
.col_done:
    ; Nueva línea
    mov al, 10
    mov [render_buffer + rcx], al
    inc rcx
    mov rcx, 0
    inc rbx
    add rsi, 1000        ; siguiente fila en universo
    jmp .row_loop
    
.row_done:
    ; Imprimir buffer
    mov rax, 1
    mov rdi, 1
    mov rsi, render_buffer
    mov rdx, rcx
    syscall
    
    pop rbx
    pop rax
    pop rcx
    pop rsi
    ret

; ------------------------------------------------------------
; Macro: render_criaturas
; Dibuja un recuadro alrededor de cada criatura detectada
; ------------------------------------------------------------
render_criaturas:
    push rsi
    push rcx
    push rax
    
    mov rcx, [num_criaturas]
    test rcx, rcx
    jz .no_criaturas
    
    mov rsi, criaturas_x
    
.print_criatura_loop:
    ; Calcular posición en pantalla
    mov rax, [criaturas_y + rsi*8]
    sub rax, [cam_y]
    add rax, 12          ; offset Y
    cmp rax, 0
    jl .next_criatura
    cmp rax, 24
    jge .next_criatura
    
    mov rbx, [criaturas_x + rsi*8]
    sub rbx, [cam_x]
    add rbx, 40          ; offset X
    cmp rbx, 0
    jl .next_criatura
    cmp rbx, 80
    jge .next_criatura
    
    ; Posición en buffer
    mov rdx, rax
    imul rdx, 81         ; asumiendo 80 + \n
    add rdx, rbx
    
    ; Poner marcador
    mov byte [render_buffer + rdx], '*'
    
.next_criatura:
    add rsi, 8
    loop .print_criatura_loop
    
.no_criaturas:
    pop rax
    pop rcx
    pop rsi
    ret

; ------------------------------------------------------------
; Macro: guardar_foto
; Guarda el buffer actual en un archivo .txt (para historial)
; ------------------------------------------------------------
%macro guardar_foto 2  ; %1 = generación, %2 = nombre_base
    push rax
    push rdi
    push rsi
    
    ; Crear nombre de archivo: generacion_xxxx.txt
    mov rdi, %1
    call int_to_string
    
    ; open / write / close (omitido por brevedad, pero implementable)
    
    pop rsi
    pop rdi
    pop rax
%endmacro

; ------------------------------------------------------------
; Macro: update_camara_con_mouse
; Permite mover la cámara (si hay input)
; ------------------------------------------------------------
%macro update_camara_con_mouse 0
    ; Leer teclas (si hay tiempo)
    ; w = arriba, s = abajo, a = izquierda, d = derecha
    ; + = zoom in, - = zoom out
    
    push rax
    push rbx
    
    mov rbx, [zoom]
    
    mov rax, 0           ; syscall read
    mov rdi, 0           ; stdin
    mov rsi, tecla_buffer
    mov rdx, 1
    syscall
    
    cmp byte [tecla_buffer], 'w'
    jne .check_s
    sub qword [cam_y], rbx
.check_s:
    cmp byte [tecla_buffer], 's'
    jne .check_a
    add qword [cam_y], rbx
.check_a:
    cmp byte [tecla_buffer], 'a'
    jne .check_d
    sub qword [cam_x], rbx
.check_d:
    cmp byte [tecla_buffer], 'd'
    jne .check_plus
    add qword [cam_x], rbx
.check_plus:
    cmp byte [tecla_buffer], '+'
    jne .check_minus
    cmp qword [zoom], 1
    jle .check_minus
    dec qword [zoom]
.check_minus:
    cmp byte [tecla_buffer], '-'
    jne .limitar
    inc qword [zoom]
; Después de mover la cámara, limitar rangos
.limitar:
    cmp qword [cam_x], 40
    jge .check_x_max
    mov qword [cam_x], 40
.check_x_max:
    cmp qword [cam_x], 960   ; 1000 - 40
    jle .check_y_min
    mov qword [cam_x], 960
.check_y_min:
    cmp qword [cam_y], 12
    jge .check_y_max
    mov qword [cam_y], 12
.check_y_max:
    cmp qword [cam_y], 988   ; 1000 - 12
    jle .done
    mov qword [cam_y], 988
.done:
    pop rdx
    pop rcx
    pop rbx
    pop rax
%endmacro

; ------------------------------------------------------------
; Función auxiliar: int_to_string (para nombres de archivo)
; ------------------------------------------------------------
int_to_string:
    push rbx
    push rcx
    push rdx
    push rsi
    
    mov rbx, 10
    mov rcx, 16          ; buffer de 16 bytes
    lea rsi, [int_buffer + 15]
    mov byte [rsi], 0
    
.loop:
    xor rdx, rdx
    div rbx
    add dl, '0'
    dec rsi
    mov [rsi], dl
    test rax, rax
    jnz .loop
    
    ; Copiar a nombre de archivo
    pop rsi
    pop rdx
    pop rcx
    pop rbx
    ret

section .bss
    tecla_buffer: resb 1
    int_buffer: resb 16
