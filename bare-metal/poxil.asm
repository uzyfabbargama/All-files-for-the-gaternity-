[bits 16]
[org 0x7c00]

inicio:
    mov ax, 0x0013 ; Modo VGA 320x200
    int 0x10
    mov ax, 0xA000 ; Apuntar al segmento de video
    mov es, ax

    ; CX = X (columna), DX = Y (fila)
    mov cx, 160
    mov dx, 100

bucle_principal:
    ; --- DIBUJAR ---
    ; Calculamos posición: DI = DX * 320 + CX
    mov ax, 320
    mul dx
    add ax, cx
    mov di, ax
    mov byte [es:di], 13 ; Pintar magenta

    ; --- ESPERAR (Sincronización básica) ---
    mov ah, 0x00
    int 0x1a      ; Leer tics del reloj del BIOS en DX
    mov bx, dx
.espera:
    int 0x1a
    cmp dx, bx
    je .espera    ; Espera a que cambie el tic (aprox 18.2 veces por seg)

    ; --- BORRAR ---
    mov byte [es:di], 0

    ; --- LÓGICA (Mover a la derecha) ---
    inc cx
    cmp cx, 319
    jne bucle_principal
    mov cx, 0     ; Reiniciar si toca el borde
    jmp bucle_principal

times 510-($-$$) db 0
dw 0xAA55
