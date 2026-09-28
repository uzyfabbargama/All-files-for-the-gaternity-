section .bss
	mem_space resb 0x3001004

;section .data
;	font_code db "var ", 0x01, 0x00, 0x00, 0x12, 0x34, 0x56, 0x78, 0x9a, ;0xbc, 0xde
global NSMotor
default rel

section .text
%define var_space 0 			; Espacio para nombres de variables
%define logic_vars 0x1000000 	; Espacio para nombres de variables lógicas y máscaras
%define loop_stack 0x2000000	; Pila para guardar las direcciones de retorno (RSI inicial)
%define loop_depth 0x2000800	; Índice del nivel actual del loop (0 a 255)
%define function_space 0x2000802; Espacio para nombres de funciones
%define function_args 0x3000802	; Espacio para argumentos
%define function_stack 0x3001002; RSI actual
%define function_depth 0x3001802; Recursión 
%define mem_total 0x3001804		; Memoria total
;=========
;KEYWORDS=
;=========
;var = 720
;proc = 1514
;decay = 2238
;growth = 5064
;logic = 2346
NSMotor:
	push rbx
	push rbp
	push r12
	push r13
	push r14
	push r15
	xor rsi, rsi 	;puntero a texto
post_start:
	xor rax, rax 	;keyword
	xor r8, r8 		;xorcompid
	xor r12, r12	;num
	xor r14, r14	;varid
	xor r13, r13	;other var
	xor r15, r15	;resultado proc
	xor rcx, rcx
	mov rax, [rdi+rsi]
	ror rax, 8
	lea rbx, [rel mem_space]
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
	mov rax, [rdi+rsi]
	ror rax, 8
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

	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14d, eax
	
	;obtenemos el número
	add rbx, var_space

	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [rdi+rsi]
	shr r12, 8
	and r12, rax
	mov [rbx+r14*8], r12
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

	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	
	;obtenemos otra variable

	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax

	;procesamos
	mov r12, [rbx+r14*8]
	mov r13, [rbx+r13*8]
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	shl r15, 1
	shr r15, 55
	and r15, 1
	mov r9, r15
	shl r14, 3
	mov [rbx+r14+7], r9b
	shr r14, 3
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	mov rax, r8
	;decay
	;decay var_ubication num
	cmp rax, 2238
	sete al
	and rax, 1
	neg rax

	;obtenemos la variable
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [rdi+rsi]
	and r12, rax
	;decaemos
	mov r13, [rbx+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	sub r13, r12
	or r13, r15
	mov [rbx+r14*8], r13

	mov rax, r8
	;growth
	;growth var_ubication num
	cmp rax, 5064
	sete al
	and rax, 1
	neg rax

	;obtenemos la variable
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [rdi+rsi]
	and r12, rax
	;decaemos
	mov r13, [rbx+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	add r13, r12
	or r13, r15
	mov [rbx+r14*8], r13

	mov rax, r8
	;logic
	cmp rax, 2346
	sete cl
	movzx rcx, cl
	add rsi, 1
	test cl, cl
	jnz pre_logic_mode1

	mov rax, r8
	xor r14, r14
	;conv 1052
	cmp rax, 1052
	setz al
	and rax, 1
	neg rax
	;sintaxis: conv n1, n2, bias
	;n1
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	;convert num
	mov r12, [rbx+r14*8]
	shr r12, 8
	and r12, rax
	;mov rcx, 7
	;and rcx, rax
	;add rsi, rcx

	;n2
	mov r13d, [rdi+rsi]
	shr r13d, 11
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	;convert num
	mov r13, [rbx+r13*8]
	shr r13, 8
	and r13, rax
	;process
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	;detect num
	mov r12, [rdi+rsi]
	shr r12, 8
	mov rcx, 7
	and rcx, rax
	and r12, rax
	add rsi, rcx
	;agregar bias
	add r15, r12
	mov [rbx+r14*8], r15

	mov r8, rax
	;norm 1162
	cmp rax, 1162
	setz al
	movzx rax, al
	neg rax
	; sintaxis
	; norm n1, n2
	; n1 y n2
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	;normalizar
	%define EPSILON 1
	mov r13, [rbx+r13*8]
	shr r13, 8
	and r13, rax
	mov r12, [rbx+r14*8]
	and r12, rax
	mov r15, r12       ; r15 = A
	xor r15, r13       ; r15 = A XOR B (diferencia de bits)
	sub r12, r15       ; A = A - (A XOR B)
	sub r13, r15       ; B = B - (A XOR B)
	sub r13, r12       ; B = B - A
	sub r15, r13       ; r15 = (A XOR B) - B
	add r15, EPSILON   ; r15 = r15 + 1 (epsilon)
	;detectar fin
	mov rax, r8
	;drop 1164
	cmp rax, 1164
	setz al
	movzx rax, al
	neg rax
	;sintaxis
	;drop n1, n2
	;n1 y n2
	mov r14d, [rdi+rsi]
	shr r14d, 11
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	mov r13d, [rdi+rsi]
	shr r13d, 11
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	;num
	mov r13, [rbx+r13*8]
	mov r12, [rbx+r14*8]
	;drop out
	mov r9, 1
	shl r9, 56
	dec r9
	shl r13, 3
	dec r13
	xor r13, r9
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	mov [rbx+r14*8], r15
	
	mov bl, [rdi+rsi]
	cmp bl, 0
	je fin
	jmp post_start
pre_logic_mode1:
	mov rax, [rdi+rsi]
	ror rax, 8
pre_logic_mode:
	;cmp = 588
	;loop = 1252
	;loopend = 9592
	;def = 632
	;edndef = 2104
	xor r8b, al
	shl r8, 1
	cmp al, 32
	setz bl
	movzx rbx, bl
	add rsi, 1
	test bl, bl
	jnz logic_mode
	shr rax, 8
	jmp pre_logic_mode
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
	mov r9d, [rdi+rsi]
	shr r9d, 8
	and r9d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	;obtener variable1
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	mov r14d, [rbx+r14*8]
	and r14, rax

	;obtener variable2
	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	xor r13, r13
	mov r13d, [rbx+r13*8]
	and r13, rax

	;sub rbx, var_space
	;add rbx, 

	;comparar si son iguales
	cmp r14, r13
	setz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov rbx, logic_vars
	mov [rbx+r9], r15
	mov rbx, var_space
	;========================================================
		; 2. logic cmpv (Compara neurona == valor constante)
		;========================================================
		; Asumiendo Hash para 'cmpv' (ejemplo: 1180)
		cmp rax, 1140
		sete al
		and rax, 1
		neg rax
;		mov rcx, 5
;		and rcx, rax
;		add rsi, rcx
	
		; Variable condicional
		mov r9d, [rdi+rsi]
		shr r9d, 8
		and r9d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Neurona
		mov r14d, [rdi+rsi]
		shr r14d, 11
		and r14d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Valor Constante (7 bytes del bytecode)
		mov r12, [rdi+rsi]
		shr r12, 8
		and r12, rax
		mov rcx, 7
		and rcx, rax
		add rsi, rcx
	
		; Comparación
		mov r14, [rbx + r14*8]
		cmp r14, r12
		setz r15b
		movzx r15, r15b
		neg r15
		and r15, rax
		mov rbx, logic_vars
		mov [rbx+r9], r15
		mov rbx, var_space
	
		;========================================================
		; 3. logic cmpn (Detecta si el byte de disparo está activo)
		;========================================================
		; Asumiendo Hash para 'cmpn' (ejemplo: 1172)
		cmp rax, 1092
		sete al
		and rax, 1
		neg rax
;		mov rcx, 5
;		and rcx, rax
;		add rsi, rcx
	
		; Variable condicional
		mov r9d, [rdi+rsi]
		shr r9d, 8
		and r9d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Neurona
		mov r14d, [rdi+rsi]
		shr r14d, 11
		and r14d, eax
		mov rcx, 3
		and rcx, rax
		add rsi, rcx
	
		; Inspeccionar únicamente el byte +7 de la neurona
		shl r14, 3
		mov al, [rbx + r14 + 7]
		test al, al
		setnz r15b
		movzx r15, r15b
		neg r15
		and r15, rax
		mov rbx, logic_vars
		mov [rbx+r9], r15
		mov rbx, var_space
		;========================================================
	    ; logic loop <var_condicional>
	    ;========================================================
	    ; Hash de 'loop' = 1252
	    cmp rax, 1252
	    sete al
	    and rax, 1
	    neg rax                      ; Máscara de ejecución
	
	    ; Obtener la variable condicional y su valor (0 o -1)
	    mov r9d, [rdi+rsi]
	    shr r9d, 8
	    and r9d, eax
	    mov rbx, logic_vars
	    mov r15, [rbx+r9]     ; r11 = variable condicional (0x0 o 0xFFFFFFFF...)
	
	    ; Registrar la dirección de inicio del bucle en la pila
	    mov rbx, loop_depth
	    mov r8, [rbx]
	    mov rbx, loop_stack
	    mov [rbx + r8*8], rsi ; Guardar RSI actual
	    mov rbx, loop_depth
	    mov rcx, 1
	    and rcx, rax
	    mov r10b, [rbx]       ; Incrementar nivel de anidación
	    add r10, rcx
	    mov [rbx], r10
	
	    mov rcx, 3
	    and rcx, rax
	    add rsi, rcx
	
	    ;========================================================
	    ; logic endloop
	    ;========================================================
	    ; Hash de 'endloop' / 'loopend' = 9592
	    cmp rax, 9592
	    sete al
	    and rax, 1
	    neg rax
	
	    ; Recuperar el RSI de inicio del bucle actual
	    mov r8, [rbx]
	    dec r8                       ; Apuntar al loop actual
	    mov rbx, loop_stack
	    mov r10, [rbx + r8*8] ; r10 = Puntero de inicio (RSI antiguo)
	
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
	    mov rbx, loop_depth
	    sub [rbx], r12        ; Resta 1 a loop_depth solo si la condición es 0
	
	    mov rcx, 1
	    and rcx, rax
	    add rsi, rcx
	    ;========================================================
    	; logic prom (Promedio entero branchless entre 2 neuronas)
    	; Sintaxis bytecode: logic prom var_destino, n1, n2
    	;========================================================
    	cmp rax, 1526
    	sete al
    	and rax, 1
    	neg rax
    	
    	; Obtener Neurona Destino
    	mov r9d, [rdi+rsi]
    	shr r9d, 8
    	and r9d, eax
    	add rsi, 3
	
    	; Obtener N1
    	mov r14d, [rdi+rsi]
    	shr r14d, 11
    	and r14d, eax
    	add rsi, 3
	
    	; Obtener N2
    	mov r13d, [rdi+rsi]
    	shr r13d, 11
    	and r13d, eax
    	add rsi, 3
	
    	; Cargar valores, sumar y desplazar (Promedio Sin Overflow)
    	mov rbx, var_space
    	mov r12, [rbx + r14*8]
    	mov r10, [rbx + r13*8]
    	add r12, r10
    	shr r12, 1               ; (n1 + n2) / 2
    	
    	mov [rbx + r9*8], r12

    	mov rax, r8
    	;def
    	;comparar
    	cmp rax, 632
    	setz al
    	movzx rax, al
    	neg al
    	;sintaxis
    	; logic def func_id (id_arg = arg)
    	;limpiar
    	xor r14, r14
    	;obtener func_id
    	mov r14d, [rdi+rsi]
    	shr r14d, 11
    	;resta 9 si es true, 0 si es false
    	mov rcx, 9
    	and rcx, rax
    	mov rdx, rsi
    	and rdx, rax
    	sub rdx, rcx
    	mov rbx, function_space
    	; Movemos la ubicación del "logic def" para volver atrás
    	mov [rbx+r14*8], rdx
    	mov rbx, function_depth
    	mov rcx, 1
    	and rcx, rax
    	mov r13b, [rbx]
    	add r13, rcx
    	mov [rbx], r13b
    	and r14, rax
    	mov rcx, 3
    	and rcx, rax
    	add rsi, rcx
    	mov dx, [rdi+rsi]
    	ror dx, 8
    	cmp dx, " ("
    	je search_args
    	
    	mov rax, r8
    	;logic yes var_cond dirno/endcond (8632)
    	xor r14, r14
    	cmp rax, 698
    	setz al
    	movzx rax, al
    	neg rax
    	mov rbx, logic_vars
    	mov r14d, [rdi+rsi]
    	shr r14d, 11
    	mov [rbx+r14*8], r11
    	mov rcx, 3
    	and rcx, rax
    	add rsi, rcx
    	mov rdx, [rdi+rsi]
    	xor rdx, rsi
    	and rdx, r11
    	xor rsi, rdx

    	;no 358
    	;logic no var_cond direndcond
    	xor r14, r14
    	mov rax, r8
    	cmp rax, 358
    	setz al
    	movzx rax, al
    	neg rax
    	mov rbx, logic_vars
    	mov r14d, [rdi+rsi]
    	shr r14d, 11
    	mov [rbx, r14*8], r11
    	mov rcx, 3
    	and rcx, rax
    	add rsi, rcx
    	mov rdx, [rsi+rdi]
    	xor rdx, rsi
    	not r11
    	and rdx, r11
    	xor rsi, rdx
    	;endef 2104
    	;logic endcond salto_a_llamada
    	mov rax, r8
    	cmp rax, 2104
    	setz al
    	movzx rax, al
    	neg rax
    	mov rbx, function_depth
    	mov rcx, 1
    	and rcx, rax
    	mov r13b, [rbx]
    	sub r13, rcx
    	mov [rbx], r13b
    	mov rbx, function_stack
    	mov [rbx+r13], rdx
    	xor rdx, rsi
    	and r14, rax
    	xor rsi, r14
    	;endcond 8632
    	mov rax, r8
    	cmp rax, 2104
    	setz al
    	movzx rax, al
    	neg rax
    	mov r14, [rdi+rsi]
    	xor r14, rsi
    	and r14, rax
    	xor rsi, r14
    	mov rcx, 7
    	and rcx, rax
    	add rsi, rcx

    	;logic use func_id
    	;use = 686
    	xor r14, r14
    	mov rax, r8
    	cmp rax, 686
    	setz al
    	movzx rax, al
    	neg rax
    	mov rdx, rsi
    	and rdx, rax
    	mov rbx, function_depth
    	mov r13b, [rbx]
    	mov rbx, function_stack
    	mov r14d, [rdi+rsi]
    	mov [rbx+r13], r14d
    	mov [rbx], dl
    
    	mov rbx, function_space
    	mov rdx, [rbx+r14*8]
    	xor rdx, rsi
    	and rdx, rax
    	xor rsi, rdx
    	mov rcx, 3
    	and rcx, rax
    	add rsi, rcx
    	jmp post_start


search_args:
    add rsi, 2
args_scan:
    mov rbx, logic_vars
    ; Leer nombre local (id_arg)
    mov r10b, [rsi+rdi]
    mov rcx, 1
    and rcx, rax
    add rsi, rcx
    
    ; Leer valor (var_logical real)
    mov r11d, [rsi+rdi]
    shr r11d, 8
    mov rcx, 3
    and rcx, rax
    add rsi, rcx
    
    ; Obtener valor REAL de la variable lógica
    mov rbx, logic_vars
    mov r12, [rbx + r11*8]       ; r12 = valor real de var_logical
    mov rbx, function_args
    mov [rbx + r10*8], r12       ; Guardar en arguments con nombre local
    
    mov dl, [rdi+rsi]
    cmp dl, ")"
    je lector_def
    jmp args_scan
lector_def:
	mov rax, [rdi+rsi]
	ror rax, 8
pre_def:
	;logic = 2346
	
	
	
	
	xor r8b, al
	shl r8, 1
	cmp al, 32
	setz bl
	movzx rbx, bl
	add rsi, 1
	test bl, bl
	jnz def_mode
	shr rax, 8
	jmp pre_def
def_mode:
	;normal
	;------
	;proc = 1514
	;decay = 2238
	;growth = 5064
	;conv = 1052
	;norm = 1162
	;drop = 1164
	mov rbx, var_space
	; proc
	mov rax, r8
	cmp rax, 1514
	setz al
	movzx rax, al
	neg rax
	;obtenemos la variable
	
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
		
	;obtenemos otra variable
	
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax
	
	;procesamos
	mov r12, [rbx+r14*8]
	mov r13, [rbx+r13*8]
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	shl r15, 1
	shr r15, 55
	and r15, 1
	mov r9, r15
	shl r14, 3
	mov [rbx+r14+7], r9b
	shr r14, 3
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	

	; logic
	mov rax, r8
	cmp rax, 2346
	je pre_local_logic1

	; decay
	mov rax, r8
	cmp rax, 2238
	setz al
	movzx rax, al
	neg rax
	;obtenemos la variable
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [rdi+rsi]
	and r12, rax
	;decaemos
	mov r13, [rbx+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	sub r13, r12
	or r13, r15
	mov [rbx+r14*8], r13


	; growth
	mov rax, r8
	cmp rax, 5064
	setz al
	movzx rax, al
	neg rax
	;obtenemos la variable
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	;obtenemos el numero
	mov cl, 3
	and rcx, rax
	add rsi, rcx
	mov r12, [rdi+rsi]
	and r12, rax
	;decaemos
	mov r13, [rbx+r14*8]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	add r13, r12
	or r13, r15
	mov [rbx+r14*8], r13

	; conv
	mov rax, r8
	cmp rax, 1052
	setz al
	movzx rax, al
	neg rax
	;conv 1052
	cmp rax, 1052
	setz al
	and rax, 1
	neg rax
	;sintaxis: conv n1, n2, bias
	;n1
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	;convert num
	mov r12, [rbx+r14*8]
	shr r12, 8
	and r12, rax
	;mov rcx, 7
	;and rcx, rax
	;add rsi, rcx

	;n2
	mov r13d, [rdi+rsi]
	shr r13d, 11
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	;convert num
	mov r13, [rbx+r13*8]
	shr r13, 8
	and r13, rax
	;process
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	;detect num
	mov r12, [rdi+rsi]
	shr r12, 8
	mov rcx, 7
	and rcx, rax
	and r12, rax
	add rsi, rcx
	;agregar bias
	add r15, r12
	mov [rbx+r14*8], r15

	; norm 
	mov rax, r8
	cmp rax, 1162
	setz al
	movzx rax, al
	neg rax
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax
	mov rcx, 3
	and rax, rcx
	add rsi, rcx
	mov r13, [rbx+r13*8]
	shr r13, 8
	and r13, rax
	mov r12, [rbx+r14*8]
	and r12, rax
	mov r15, r12       ; r15 = A
	xor r15, r13       ; r15 = A XOR B (diferencia de bits)
	sub r12, r15       ; A = A - (A XOR B)
	sub r13, r15       ; B = B - (A XOR B)
	sub r13, r12       ; B = B - A
	sub r15, r13       ; r15 = (A XOR B) - B
	add r15, EPSILON   ; r15 = r15 + 1 (epsilon)

	; drop
	mov rax, r8
	cmp rax, 1164
	setz al
	movzx rax, al
	neg rax
;n1 y n2
	mov r14d, [rdi+rsi]
	shr r14d, 11
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	mov r13d, [rdi+rsi]
	shr r13d, 11
	mov rcx, 3
	and rax, rcx
	add rsi, rcx

	;num
	mov r13, [rbx+r13*8]
	mov r12, [rbx+r14*8]
	;drop out
	mov r9, 1
	shl r9, 56
	dec r9
	shl r13, 3
	dec r13
	xor r13, r9
	mov r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	mov [rbx+r14*8], r15

pre_local_logic1:
	mov rax, [rdi+rsi]
	ror rax, 8
pre_local_logic:
	xor r8b, al
	shl r8, 1
	cmp al, 32
	setz bl
	movzx rbx, bl
	add rsi, 1
	test bl, bl
	jnz local_logic
	shr rax, 8
	jmp pre_local_logic
local_logic:
	;cmp = 588
	mov rax, r8
	cmp rax, 588
	setz al
	movzx rax, al
	neg rax
;obtener variable condicional
	mov r9d, [rdi+rsi]
	shr r9d, 8
	and r9d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	;obtener variable1
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	mov r14d, [rbx+r14*8]
	and r14, rax

	;obtener variable2
	mov r13d, [rdi+rsi]
	shr r13d, 11
	and r13, rax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx
	mov r13d, [rbx+r13*8]
	and r14, rax

	;sub rbx, var_space
	;add rbx, 

	;comparar si son iguales
	cmp r14, r13
	setz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov rbx, function_args
	mov [rbx+r9], r15
	mov rbx, var_space
	
	;loop = 1252
	mov rax, r8
	cmp rax, 1252
	setz al
	movzx rax, al
	neg rax
    ; Obtener la variable condicional y su valor (0 o -1)
    mov r9d, [rdi+rsi]
    shr r9d, 8
    and r9d, eax
    mov rbx, function_args
    mov r15, [rbx+r9]     ; r11 = variable condicional (0x0 o 0xFFFFFFFF...)

    ; Registrar la dirección de inicio del bucle en la pila
    mov rbx, loop_depth
    mov r8, [rbx]
    mov rbx, loop_stack
    mov [rbx + r8*8], rsi ; Guardar RSI actual
    mov rbx, loop_depth
    inc qword [rbx]       ; Incrementar nivel de anidación

    mov rcx, 3
    and rcx, rax
    add rsi, rcx


	;loopend = 9592
	mov rax, r8
	cmp rax, 9592
	setz al
	movzx rax, al
	neg rax
    ; Recuperar el RSI de inicio del bucle actual
    mov r8, [rbx]
    dec r8                       ; Apuntar al loop actual
    mov rbx, loop_stack
    mov r10, [rbx + r8*8] ; r10 = Puntero de inicio (RSI antiguo)

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
    mov rbx, loop_depth
    sub [rbx], r12        ; Resta 1 a loop_depth solo si la condición es 0

    mov rcx, 1
    and rcx, rax
    add rsi, rcx

	;cmpv = 1140
	mov rax, r8
	cmp rax, 1140
	setz al
	movzx rax, al
	neg rax
	; Variable condicional
	mov r9d, [rdi+rsi]
	shr r9d, 8
	and r9d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	; Neurona
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	; Valor Constante (7 bytes del bytecode)
	mov r12, [rdi+rsi]
	shr r12, 8
	and r12, rax
	mov rcx, 7
	and rcx, rax
	add rsi, rcx

	; Comparación
	mov r14, [rbx + r14*8]
	cmp r14, r12
	setz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov rbx, function_args
	mov [rbx+r9], r15
	mov rbx, var_space

	;cmpn = 1092
	mov rax, r8
	cmp rax, 1092
	setz al
	movzx rax, al
	neg rax
	; Variable condicional
	mov r9d, [rdi+rsi]
	shr r9d, 8
	and r9d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	; Neurona
	mov r14d, [rdi+rsi]
	shr r14d, 11
	and r14d, eax
	mov rcx, 3
	and rcx, rax
	add rsi, rcx

	; Inspeccionar únicamente el byte +7 de la neurona
	shl r14, 3
	mov al, [rbx + r14 + 7]
	test al, al
	setnz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov rbx, function_args
	mov [rbx+r9], r15
	mov rbx, var_space

	;yes = 698
	mov rax, r8
	cmp rax, 698
	setz al
	movzx rax, al
	neg rax
   	mov rbx, function_args
   	mov r14d, [rdi+rsi]
  	shr r14d, 11
   	mov [rbx+r14*8], r11
   	mov rcx, 3
   	and rcx, rax
   	add rsi, rcx
   	mov rdx, [rdi+rsi]
   	xor rdx, rsi
   	and rdx, r11
   	xor rsi, rdx

	;no = 358
	mov rax, r8
	cmp rax, 358
	setz al
	movzx rax, al
	neg rax
   	mov rbx, function_args
   	mov r14d, [rdi+rsi]
   	shr r14d, 11
   	mov [rbx, r14*8], r11
   	mov rcx, 3
   	and rcx, rax
   	add rsi, rcx
   	mov rdx, [rsi+rdi]
   	xor rdx, rsi
   	not r11
   	and rdx, r11
   	xor rsi, rdx

	;endcond = 8632
	mov rax, r8
	cmp rax, 8632
	setz al
	movzx rax, al
	neg rax
   	mov r14, [rdi+rsi]
   	xor r14, rsi
   	and r14, rax
   	xor rsi, r14
   	mov rcx, 7
   	and rcx, rax
   	add rsi, rcx

	;prom = 1526
	mov rax, r8
	cmp rax, 1526
	setz al
	movzx rax, al
	neg rax
   	; Obtener Neurona Destino
   	mov r9d, [rdi+rsi]
   	shr r9d, 8
   	and r9d, eax
   	add rsi, 3

   	; Obtener N1
   	mov r14d, [rdi+rsi]
   	shr r14d, 11
   	and r14d, eax
   	add rsi, 3

   	; Obtener N2
   	mov r13d, [rdi+rsi]
   	shr r13d, 11
   	and r13d, eax
   	add rsi, 3

   	; Cargar valores, sumar y desplazar (Promedio Sin Overflow)
   	mov rbx, var_space
   	mov r12, [rbx + r14*8]
   	mov r10, [rbx + r13*8]
   	add r12, r10
   	shr r12, 1               ; (n1 + n2) / 2
   	
   	mov [rbx + r9*8], r12

	;logic endef = 2104
	mov rax, r8
	cmp rax, 2104
	setz dl
	setz al
	movzx rax, al
	neg rax
	mov rcx, 11
	and rcx, rax
	sub rsi, rcx ;volver atrás
	test dl, dl
	;salir del modo función y ejecutar todo del endef
	jnz post_start

	;logic def = 632
	mov rax, r8
	cmp rax, 632
	setz dl
	setz al
	movzx rax, al
	neg rax
	mov rcx, 9
	and rcx, rax
	sub rsi, rcx
	test dl, dl
	jnz post_start

	jmp def_mode
fin:
    ; Restaurar registros y retornar a Python
    pop r15
    pop r14
    pop r13
    pop r12
    pop rbp
    pop rbx
    ret
