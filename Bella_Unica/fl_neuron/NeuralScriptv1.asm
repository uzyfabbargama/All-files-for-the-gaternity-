section .bss
	var_space resb 0x1000000
	logic_vars resb 0x1000000
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
	xor r8, al
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
	mov [var_space+r14], r12
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
	mov r12, [var_space+r14]
	mov r13, [var_space+r13]
	or r15, r12
	and r15, r13
	add r12, r15
	add r13, r15
	add r13, r12
	add r15, r13
	shl r15, 1
	shr r15, 63
	mov r9, r15
	mov [var_space+r14+7], r9b
	mov rcx, 3
	and rcx, rax
	add rsi, rax

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
	mov r13, [var_space+r14]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	sub r13, r12
	or r13, r15
	mov [var_space+r14], r13

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
	mov r13, [var_space+r14]
	mov r15, r13
	shr r15, 56
	shl r15, 56
	shr r13, 8
	add r13, r12
	or r13, r15
	mov [var_space+r14], r13

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
	jmp manage_state
pre_logic_mode1:
	mov rax, [font_code+rsi]
pre_logic_mode:
	;cmp = 588
	;loop = 1252
	;loopend = 9592
	;def = 632
	;edndef = 2104
	xor r8, al
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
	;obtener variable condicional
	mov r9d, [font_code+rsi]
	shr r9d, 8
	and r9d, rax

	;obtener variable1
	mov r14d, [font_code+rsi]
	shr r9d, 8
	and r14, rax

	;obtener variable2
	mov r13d, [font_code+rsi]
	shr r9d, 8
	and r13, rax

	;comparar si son iguales
	cmp r14, r13
	setz r15b
	movzx r15, r15b
	neg r15
	and r15, rax
	mov [logic_vars+r9], r15
	jmp manage_state
fin: 
	xor rdi, rdi
	mov rax, 60
	syscall
