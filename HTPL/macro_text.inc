%macro take_line 0
    ;r10 = start/end/nesting
    ;r13 tiene la línea, el inicio, el final y el anidamiento del dato, y el objetivo es que r13 sólo guarde la línea, mientras que r10 tiene el resto de los datos
    mov r10, r13
    ;aquí r9 obtiene la máscara de 48 bytes para preservar el start end y nesting
    mov r9, 0xFFFFFFFF
    shl r9, 4
    or r9, 0xFFFF
    ;aquí r10 borra el dato de la línea
    and r10, r9
    ;aquí r13 tiene sólo el dato de la línea
    shr r13, 48
    and r13, 0xFFFF
%endmacro
%macro desempaquetar_variable 0
	;aquí r13 (la línea de la variable) intercambia valor con la línea actual
    xor r13, rdx
    xor rdx, r13
    xor r13, rdx
    ;ahora guardamos igual el rsi, para poder volver después
    xor rbx, rsi
    xor rsi, rbx
    xor rbx, rsi
    ;ahora sabiendo que r10 tiene el start, el end y el nesting
    ;obtenemos el start en r9
    mov r9, r10 ;start
    shr r9, 32
    and r9, 0xFFFF
    
    ;obtenemos el end en r8
    mov r8, r10 ;end
    shr r8, 16
    and r8, 0xFFFF
    
    ;obtenemos el nesting en r11
    mov r11, r10 ;nesting
    and r11, 0xFFFF
    
    ;movemos el valor de la línea actual a un acumulador para posteriormente desplazar por 6, sumarle el start, y mover el start a un contador para comparar con el final 
    mov rax, rdx
    shl rax, 6
    add rax, r9
    mov cx, r9w
    
    ;ahora con el valor listo en rax, lo movemos al puntero en rsi, y borramos el r9 que ya usamos
    mov rsi, rax
    xor r9, r9
%endmacro
%macro selector_data_type 0
	;Movemos el primer byte para luego detectar si realmente comienza con " o ' (para luego compararlo con xorid), pero sino, tomamos los 8 bytes directamente donde está el número
    mov al, [rsi+font_code]
    movzx rax, al
    cmp al, '"'
    je %%text
    cmp al, "'"
    je %%text
    mov rax, [rsi+font_code]
    %%text:
        xor r9, al
        shl r9, 1
        inc cx
        cmp cx, r8
        je %%exit
        jmp %%text
    %%exit:
%endmacro
%macro volver_al_pasado 0
	;como antes el valor del RSI estaba en rbx, lo volvemos, y también la línea actual
	mov rsi, rbx
	mov rdx, r13
%endmacro

%macro buscar 0
	mov al, [font_code+rsi]
	cmp al, '"'
	je %%text
	cmp al, "'"
	....
%macro comparar 0
	;Aquí ponemos las definiciones
	;==
	%define KW_equality 142
	;>=
	%define KW_more_then 130 
	;<=
	%define KW_less_then 138
	;!=
	%define KW_not_then 254
	;aqui obtenemos el valor actual (y bueno, hace un montón de cosas más)
	id_variable
	cmp r14, KW_equality
	je %%equal
	cmp r14, KW_more_then
	je %%amount
	cmp r14, KW_less_then
	je %%amount
	cmp r14, KW_not_then
	je %%equal
	%%equal:
		;aquí comparamos igualdad
		xor r8, r8
		cmp r15, r9
		setz r8b
		cmp r15, r9
