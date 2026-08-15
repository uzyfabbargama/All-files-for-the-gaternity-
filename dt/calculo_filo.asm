section .data
	filename: db "image.raw", 0
section .bss
	fd: resq 1
	buffer: resb 4096
	count: resq 1
section .text
	global _start
	
_start:
%macro abrir_archivo 0
	mov rax, 257
	mov rdi, -100
	mov rsi, filename
	xor rdx, rdx
	xor r10, r10
	syscall
	mov [fd], rax
%endmacro

%macro leer_archivo 0
	mov rax, 0
	mov rdi, [fd]
	mov rsi, buffer
	mov rdx, 4096
	syscall
%endmacro

%macro cerrar_archivo 0
	mov rax, 3
	mov rdi, [fd]
	syscall
%endmacro

%macro salir 0
	mov rax, 60
	xor rdi, rdi
	syscall
%endmacro
	%define up -256
	%define down 256
	%define left -1
	%define right 1
	%define upleft -257
	%define upright -255
	%define downleft 255
	%define downright 257
	%define center 0
	;r13 → 1, 2
	;r14 → 3, 4
	;r15 → 5, 6
	;r11 → 7, 8
	;r8 → 9
%macro tomar_pixeles 3
	; tomar primer píxel
	mov eax, [buffer+%2+rsi]
	mov %1, eax
	shl %1, 32
	; tomar segundo píxel
	mov eax, [buffer+%3+rsi]
	mov %1, eax
%endmacro

%macro tomar_centro 2
	mov eax, [buffer+%2+rsi]
	mov %1, eax
%endmacro
;%define red 0
;%define green 8
;%define blue 16
%define alpha 24
;%macro comparar_bytes 3
;	%assign value %2
;	%assign bytes %3
;	%assign maskbit (1-value&((bytes<<8)-1))
;	add %1, maskbit
;	shr %1, 8
;	and %1, 1
;%endmacro
%macro procesar_alpha 2
	;%1 = registro
	;%2 = registro central
	;tomar registro
	mov r9, %1 
	;buscar alpha
	shr r9, alpha 
	and r9, 0xff
	comparar_bytes r9, 0, 1 ;es r9 => 0 en alpha
	add %2, 1
%endmacro
