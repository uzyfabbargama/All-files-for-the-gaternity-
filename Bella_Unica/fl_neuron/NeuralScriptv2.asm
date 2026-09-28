section .bss
	var_space resb 0x1000000 ; espacio para nombres de variables
	logic_vars resb 0x1000000; espacio para nombres de variables lógicas y máscaras
	loop_stack   resq 256    ; Pila para guardar las direcciones de retorno (RSI inicial)
	loop_depth   resq 1      ; Índice del nivel actual del loop (0 a 255)
section .data
	font_code db "var ", 0x01, 0x00, 0x00, 0x12, 0x34, 0x56, 0x78, 0x9a, 0xbc, 0xde
section .text

global _start
;=========
;KEYWORDS=
;=========
;var = 720
;proc = 1514
;decay = 2238
;growth = 5064
;logic = 2346
_start:
	xor rsi, rsi 	;puntero a texto
post_start:
	xor rax, rax 	;keyword
	xor r8, r8 		;xorcompid
	xor r12, r12	;num
	xor r14, r14	;varid
	xor r13, r13	;other var
	xor r15, r15	;resultado proc
	xor rcx, rcx
	mov rax, [font_code+rsi]
start_parser:
	xor r8b, al
	shl r8, 1
	cmp al, 32
	shr rax, 8
	je manager_state
	add rsi, 1
	add cl, 1
	cmp cl, 8
	je .next
	jmp start_parser
.next:
	mov rax, [font_code+rsi]
	jmp start_parser
manager_state:
	add rsi, 1
	mov rax, r8
	;var
	;var var_ubication num
	cmp rax, 720
	sete al
	and rax, 1
	neg rax
	;obtenemos la variable

	mov r14d, [font_code+rsi]
	shr r14d, 8
	and r14d, eax
	
	;obtenemos el número

	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [font_code+rsi]
	shr r12, 8
	and r12, rax
	mov [var_space+r14*8], r12
	mov cl, 7
	and rcx, rax
	add rsi, rcx

	mov rax, r8
	;proc
	;proc var_ubication var_ubication2
	cmp rax, 1514
	sete al
	and rax, 1
	neg rax
	;obtenemos la variable

	mov r14d, [font_code+rsi]
	shr r14d, 8
	and r14, rax
	
	;obtenemos otra variable

	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r13d, [font_code+rsi]
	shr r13d, 8
	and r13, rax

	;procesamos
	mov r12, [var_space+r14*8]
	mov r13, [var_space+r13*8]
	or r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	shl r15, 1
	shr r15, 55
	mov r9, r15
	shl r14, 3
	mov [var_space+r14+7], r9b
	shr r14, 3
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	mov rax, r8
	;decay
	;decay var_ubication num
	cmp rax, 2338
	sete al
	and rax, 1
	neg rax

	;obtenemos la variable
	mov r14d, [font_code+rsi]
	shr r14d, 8
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [font_code+rsi]
	and r12, rax
	;decaemos
	mov r13, [var_space+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	sub r13, r12
	or r13, r15
	mov [var_space+r14*8], r13

	mov rax, r8
	;growth
	;growth var_ubication num
	cmp rax, 5064
	sete al
	and rax, 1
	neg rax

	;obtenemos la variable
	mov r14d, [font_code+rsi]
	shr r14d, 8
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [font_code+rsi]
	and r12, rax
	;decaemos
	mov r13, [var_space+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	add r13, r12
	or r13, r15
	mov [var_space+r14*8], r13

	mov rax, r8
	;logic
	cmp rax, 2346
	sete cl
	movzx rcx, cl
	add rsi, 1
	test cl, cl
	jnz pre_logic_mode1
	mov bl, [font_code+rsi]
	cmp bl, 0
	je fin
	jmp manager_state
pre_logic_mode1:
	mov rax, [font_code+rsi]
pre_logic_mode:
	;cmp = 588
	;loop = 1252
	;loopend = 9592
	;def = 632
	;edndef = 2104
	xor r8b, al
	shl r8, 1
	cmp al, 32
	shr rax, 8
	je logic_mode
	add rsi, 1
	jmp start_parser
logic_mode:
	mov rax, r8
	;cmp
	;logic cmp var_conditional var_ubication var_ubication2
	cmp rax, 588
	sete al
	and rax, 1
	neg rax
	mov rcx, 4
	and rcx, rax
	add rsi, rcx
	;obtener variable condicional
	mov r9d, [font_code+rsi]
	shr r9d, 8
	and r9d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	;obtener variable1
	mov r14d, [font_code+rsi]
	shr r14d, 8
	and r14, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	mov r14d, [var_space+r14*8]
	and r14, rax

	;obtener variable2
	mov r13d, [font_code+rsi]
	shr r13d, 8
	and r13, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	mov r13d, [var_space+r13*8]
	and r14, rax

	;comparar si son iguales
	cmp r14, r13
	setz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov [logic_vars+r9], r15
	jmp post_start
	;========================================================
		; 2. logic cmpv (Compara neurona == valor constante)
		;========================================================
		; Asumiendo Hash para 'cmpv' (ejemplo: 1180)
		cmp rax, 1140
		sete al
		and rax, 1
		neg rax
		mov rcx, 5
		and rcx, rax
		add rsi, rcx
	
		; Variable condicional
		mov r9d, [font_code+rsi]
		shr r9d, 8
		and r9d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Neurona
		mov r14d, [font_code+rsi]
		shr r14d, 8
		and r14d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Valor Constante (8 bytes del bytecode)
		mov r12, [font_code+rsi]
		and r12, rax
		mov rcx, 8
		and rcx, rax
		add rsi, rcx
	
		; Comparación
		mov r14, [var_space + r14*8]
		cmp r14, r12
		setz r15b
		movzx r15, r15b
		neg r15
		and r15, rax
		mov [logic_vars+r9], r15
		jmp post_start
	
		;========================================================
		; 3. logic cmpn (Detecta si el byte de disparo está activo)
		;========================================================
		; Asumiendo Hash para 'cmpn' (ejemplo: 1172)
		cmp rax, 1092
		sete al
		and rax, 1
		neg rax
		mov rcx, 5
		and rcx, rax
		add rsi, rcx
	
		; Variable condicional
		mov r9d, [font_code+rsi]
		shr r9d, 8
		and r9d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Neurona
		mov r14d, [font_code+rsi]
		shr r14d, 8
		and r14d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Inspeccionar únicamente el byte +7 de la neurona
		shl r14, 3
		mov bl, [var_space + r14 + 7]
		test bl, bl
		setnz r15b
		movzx r15, r15b
		neg r15
		and r15, rax
		mov [logic_vars+r9], r15
		jmp post_start
		;========================================================
	    ; logic loop <var_condicional>
	    ;========================================================
	    ; Hash de 'loop' = 1252
	    cmp rax, 1252
	    sete al
	    and rax, 1
	    neg rax                      ; Máscara de ejecución
	
	    ; Obtener la variable condicional y su valor (0 o -1)
	    mov r9d, [font_code+rsi]
	    shr r9d, 8
	    and r9d, eax
	    mov r11, [logic_vars+r9]     ; r11 = variable condicional (0x0 o 0xFFFFFFFF...)
	
	    ; Registrar la dirección de inicio del bucle en la pila
	    mov r8, [loop_depth]
	    mov [loop_stack + r8*8], rsi ; Guardar RSI actual
	    inc qword [loop_depth]       ; Incrementar nivel de anidación
	
	    mov rcx, 3
	    and rcx, rax
	    add rsi, rcx
	    jmp post_start
	
	    ;========================================================
	    ; logic endloop
	    ;========================================================
	    ; Hash de 'endloop' / 'loopend' = 9592
	    cmp rax, 9592
	    sete al
	    and rax, 1
	    neg rax
	
	    ; Recuperar el RSI de inicio del bucle actual
	    mov r8, [loop_depth]
	    dec r8                       ; Apuntar al loop actual
	    mov r10, [loop_stack + r8*8] ; r10 = Puntero de inicio (RSI antiguo)
	
	    ;--------------------------------------------------------
	    ; Tu fórmula branchless:
	    ; xor puntero_loop, puntero_actual  -> r10 ^ rsi
	    ; and puntero_loop, var_cond        -> (r10 ^ rsi) & r11
	    ; xor puntero_actual, puntero_loop  -> rsi ^ ...
	    ;--------------------------------------------------------
	    xor r10, rsi                 ; r10 = r10 ^ rsi
	    and r10, r11                 ; Apaga la diferencia si r11 es 0
	    xor rsi, r10                 ; Si r11 es -1, RSI vuelve al inicio. Si r11 es 0, no cambia.
	
	    ; Si el bucle NO se repite (r11 == 0), liberamos el nivel de la pila
	    ; Hacemos el ajuste de loop_depth también de forma branchless:
	    mov r12, r11
	    not r12                      ; r12 = -1 si el loop terminó, 0 si continúa
	    and r12, 1
	    sub [loop_depth], r12        ; Resta 1 a loop_depth solo si la condición es 0
	
	    mov rcx, 1
	    and rcx, rax
	    add rsi, rcx
	    jmp post_start
fin: 
	xor rdi, rdi
	mov rax, 60
	syscall
