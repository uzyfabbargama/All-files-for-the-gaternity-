section .data
	;draw x, y
	;
	;
	;
	;
	;
	font_code dq "draw 1, 2", 10
section .bss
	vars: resb 0x1000000
	pantalla: resb 0x1fa4000
	lines: resb 8*256
section .text
	global _start
_start:
	%define x 1
	%define y 1080
	
	%define SYS_MAP 		9
	%define PROT_READ 		0x1
	%define PROT_WRITE 		0x2
	%define MAP_PRIVATE 	0x2
	%define MAP_ANONYMOUS 	0x20
	%define LINE_LIMIT		0x1000
	;draw
	%define kw_draw 1210
	xor rsi, rsi
	xor rcx, rcx
	%macro transpiler 3
		; 1. tomar del código fuente
		mov al, font_code[rsi]
		; 2. buscar el fin de linea
		cmp al, 10
		jz %1
		; 3. mover la línea
		mov line[rsi], al
		; 4. actualizar el contador de línea
		add rcx, 1
		add rsi, 1
		; 5. ¿es 32?
		mov r9, rcx
		shr r9, 5 ; 32 >> 5
		and r9, 1
		jnz %3
		jmp %2
	%endmacro
alloc_dynamic_memory:
	push rsi
	mov rax, SYS_MMAP		; syscll number 9
	xor rdi, rdi			; addr = NULL (el kernel elige la dirección)
	mov rsi, LINE_LIMIT		; lenght = tamaño deseado en bytes (el código)
	mov rdx, PROT_READ | PROT_WRITE ; prot = lectura y escritura
	mov r10, MAP_PRIVATE | MAP_ANONYMOUS ; flags = memoria privada e independiente de archivo
	mov r8, -1 				; fd = -1 (requerido para MAP_ANONYMOUS)
	xor r9, r9				; offset 0
	syscall					; listo
	pop rsi
	mov line[rsi], rax		; guardador de líneas
	
transpilar:
	transpiler exit, transpilar, alinear
exit:
    push rax
    push rdi
    push rsi
    push rdx
    mov rax, 1
    mov rdi, 1
    mov rsi, line
    mov rdx, 32
    syscall
    pop rdx
    pop rsi
    pop rdi
    pop rax
	xor rdi, rdi
	mov rax, 60
	syscall
alinear:
	mov r9, rcx
	sub r9, 32
	add rcx, r9
