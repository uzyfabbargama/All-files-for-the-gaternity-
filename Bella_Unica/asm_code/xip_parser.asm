%include "start.inc"
next_char:
    movzx rdx, byte [rdi + rsi] 
    test dl, dl                 
    jz exit_parse
    jmp rbx    ; Saltamos directamente a donde r15 diga. Sin preguntas. ; --- EL GRAN SALTO ---
modo_id:
	; Si dl <= 32 (espacio, \n, \r, tab), simplemente lo saltamos 
    ; y no dejamos que XORID lo toque.
    cmp dl, 10
    je .skip_basura
    ; --- 1. DETECTOR DE TRAMA (Prioridad) ---
    xif 0, 156   ; Detecta "::" (listo)
    test r9, r9
    jnz cambiar_a_mem ;Si hay "::", cambiamos el puntero
    
    xorid               ; Procesamos el carácter del nombre
    inc rsi
    jmp next_char
