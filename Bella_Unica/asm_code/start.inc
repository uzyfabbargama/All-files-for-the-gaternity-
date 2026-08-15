    ; ... (Set inicial r10, rsi, r14, r15, r12 igual) ...
	; --- 1. SET INICIAL (EL CORAZÓN DEL MOTOR) ---
    mov r10, rsi  ; rsi entra con la dirección de 'self.mente' desde Python
    xor rsi, rsi  ; Limpiamos rsi para usarlo como índice del string (RDI)
    xor r14, r14  ; ID = 0
    xor r15, r15  ; Mapa de estados = 0
    xor r12, r12  ; Acumulador de valor = 0
    lea rbx, [rel modo_id]    ; Usamos RBX para el salto (dejamos R15 libre o lo ignoramos)
