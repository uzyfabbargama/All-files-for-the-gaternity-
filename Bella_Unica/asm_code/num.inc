    xif_flex 1, 452   ; Detecta ",,"
    test r9, r9
    jnz cambiar_a_id
    if_num 1, "1" ;(listo)
    if_num 2, "2"
    if_num 3, "3"
    if_num 4, "4"
    if_num 5, "5"
    if_num 6, "6"
    if_num 7, "7"
    if_num 8, "8"
    if_num 9, "9"
    if_num 0, "0"
    if_num 0, 0x20
	inc rsi
    jmp next_char
