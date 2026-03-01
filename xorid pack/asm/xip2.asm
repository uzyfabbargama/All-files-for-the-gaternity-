section .text
global _xip_parse

_xip_parse:
    ; --- INICIALIZACIÓN ---
    xor rsi, rsi
    xor r14, r14
    xor r15, r15
    xor r12, r12

next_char:
    movzx rdx, byte [INPUT + rsi] ; Cargar byte actual
    test rdx, rdx                 ; ¿Fin de archivo?
    jz exit_parse

    ; --- CAPA 1: DETECCIÓN DE TOKENS (Tus macros xif) ---
    xif 0, 156   ; Busca "::"
    do_in r15    ; Si lo halla, bit 0 de r15 = 1
    skip         ; Avanza rsi si r9=1
    
    xif 1, 232   ; Busca ",,"
    do_in r15    ; Si lo halla, bit 1 de r15 = 1
    skip         ; Avanza rsi si r9=1

    ; --- CAPA 2: LÓGICA DE DECISIÓN (elsecond) ---
    ; Aquí usamos tu macro para decidir si ejecutamos xorid o mul_10
    elsecond 0, r15 ; Si bit 0 de r15 es 0, r9 se activa para xorid
    
    ; --- CAPA 3: EJECUCIÓN ARITMÉTICA ---
    xorid        ; Solo procesa la key si r9 dice que no hay "::" aún
    
    ; --- CAPA 4: PROCESAMIENTO DE VALORES ---
    ; (Aquí iría tu bloque de if_num 0-9 para llenar r12)
    
    inc rsi      ; Siguiente byte
    jmp next_char

exit_parse:
    ret
